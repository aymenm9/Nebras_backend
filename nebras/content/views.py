from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .models import Metadata, YoutubeVideo, R2File, MultipartUpload, Part
from .serializers import MetadataSerializer, YoutubeVideoSerializer, R2FileSerializer,PartSerializer, MultipartUploadSerializer, MultipartUploadResponseSerializer, SimpleUploadResponseSerializer
from .utils import generate_presigned_url, complete_r2_file, get_next_part_number, generate_presigned_url_for_part, abort_s3_multipart_upload, delete_s3_object
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer
from rest_framework.throttling import ScopedRateThrottle
# Create your views here.

class UploadYoutubeVideo(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'uploads'
    serializer_class = YoutubeVideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type','metadata__is_listed']
    search_fields = ['metadata__title','metadata__description']
    queryset = YoutubeVideo.objects.all()

    def get_queryset(self):
        return YoutubeVideo.objects.filter(metadata__created_by=self.request.user)

class UploadYoutubeVideoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = YoutubeVideoSerializer
    queryset = YoutubeVideo.objects.all()
    
    def get_queryset(self):
        return YoutubeVideo.objects.filter(metadata__created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.metadata.delete()


class R2FileUpload(generics.ListCreateAPIView):
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'uploads'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type', 'upload_type','metadata__is_listed']
    search_fields = ['metadata__title','metadata__description']
    queryset = R2File.objects.all()

    def get_queryset(self):
        return R2File.objects.filter(metadata__created_by=self.request.user)

class R2FileUploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = R2FileSerializer
    queryset = R2File.objects.all() # dont filter here let the moderator see all his files
    
    def get_queryset(self):
        return R2File.objects.filter(metadata__created_by=self.request.user)

    def perform_destroy(self, instance):
        if instance.upload_type == 'multipart':
            if instance.upload_status != 'completed' and hasattr(instance, 'multipart_uploader') and instance.multipart_uploader.upload_id:
                abort_s3_multipart_upload(instance.file_key, instance.multipart_uploader.upload_id)
            else:
                delete_s3_object(instance.file_key)
        else:
            delete_s3_object(instance.file_key)
        
        instance.metadata.delete()


class MultipartUploadDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = MultipartUploadSerializer
    queryset = MultipartUpload.objects.all()
    
    def get_queryset(self):
        return MultipartUpload.objects.filter(r2_file__metadata__created_by=self.request.user)


class GetUploadURL(views.APIView):
    # this will work with bouth 
    # if upload_type is multipart it will return the presigned url for the next part to upload "or can make it 2-3 at time but for now just one"
    # if upload_type is simple it will return the presigned url for the file
    permission_classes = [IsAuthenticated,IsModerator]
    
    @extend_schema(
        request=None,
        responses={
            200: PolymorphicProxySerializer(
                component_name='UploadURLResponse',
                serializers={
                    'multipart': MultipartUploadResponseSerializer,
                    'simple': SimpleUploadResponseSerializer,
                },
                resource_type_field_name='upload_type', # Optional: helps UI switch types
            ),
            404: None,
            403: None,
        },
        description="Get the presigned upload URL for either multipart or simple uploads."
    )
    def post(self, request, pk:int):
        # get the R2file
        try:
            r2_file = R2File.objects.get(id=pk)
        except R2File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if r2_file.metadata.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if r2_file.upload_type == 'multipart':
            next_part_number = get_next_part_number(r2_file.multipart_uploader)
            presigned_url = generate_presigned_url_for_part(r2_file,part_number=next_part_number)
            return Response({'presigned_url': presigned_url, 'next_part_number': next_part_number}, status=status.HTTP_200_OK)
        else:
            presigned_url = generate_presigned_url(r2_file, method='put_object')
            return Response({'presigned_url': presigned_url}, status=status.HTTP_200_OK)
            

class PartCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = PartSerializer

class PartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = PartSerializer
    queryset = Part.objects.all()
    
    def get_queryset(self):
        return Part.objects.filter(multipart_upload__r2_file__metadata__created_by=self.request.user)

    def perform_destroy(self, instance):
        # We don't abort the entire multipart upload just because one part gets deleted.
        # R2 will automatically clean up incomplete parts after a lifecycle policy completes (usually).
        # We just remove the part record and decrement the uploaded part counter safely or leave it to be recreated.
        multipart_upload = instance.multipart_upload
        super().perform_destroy(instance)
        # Fix counter if we delete a part
        if multipart_upload.uploaded_parts > 0:
            multipart_upload.uploaded_parts -= 1
            multipart_upload.save()

class CompleteMultipartUpload(views.APIView): 
    permission_classes = [IsAuthenticated,IsModerator]
    
    @extend_schema(
        request=None,
        responses={200: R2FileSerializer, 404: None, 403: None, 400: "Not all parts are completed in the multipart upload"},
        description="Complete the multipart upload"
    )
    def post(self, request, pk:int):
        try:
            r2_file = R2File.objects.get(id=pk)
        except R2File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if r2_file.metadata.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not complete_r2_file(r2_file):
            return Response({'error': 'Not all parts are completed in the multipart upload'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(R2FileSerializer(r2_file).data,status=status.HTTP_200_OK)

    