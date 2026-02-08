from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from .models import Metadata, YoutubeVideo, R2File, MultipartUpload, Part
from .serializers import MetadataSerializer, YoutubeVideoSerializer, R2FileSerializer, R2FileSerializerUpload,PartSerializer, MultipartUploadSerializer
from .utils import generate_presigned_url
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# Create your views here.

class UploadYoutubeVideo(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = YoutubeVideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type']
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


class R2FileUpload(generics.ListAPIView):
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type']
    search_fields = ['metadata__title','metadata__description']
    queryset = R2File.objects.all()

    def get_queryset(self):
        return R2File.objects.filter(metadata__created_by=self.request.user)

class R2FileUploadCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = R2FileSerializerUpload
    


class R2FileUploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = R2FileSerializer
    queryset = R2File.objects.all().filter(upload_completed=True)
    
    def get_queryset(self):
        return R2File.objects.filter(metadata__created_by=self.request.user)

# the multipart upload views is for biger files give 2 main binifit upload and resume upload and in normal presigned url upload we can't upload MORE than 5GB files

class MultipartUploadCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = MultipartUploadSerializer

class MultipartUploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = MultipartUploadSerializer
    queryset = MultipartUpload.objects.all()
    
    def get_queryset(self):
        return MultipartUpload.objects.filter(r2_file__metadata__created_by=self.request.user)

class PartCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = PartSerializer

class PartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = PartSerializer
    queryset = Part.objects.all()
    
    def get_queryset(self):
        return Part.objects.filter(multipart_upload__r2_file__metadata__created_by=self.request.user)

class CompleteMultipartUpload(views.APIView): 
    permission_classes = [IsAuthenticated,IsModerator]
    
    # extend_schema(
    #    request={

    #    },
    #    responses={200: R2FileSerializer}
    # )
    def post(self, request):
        multipart_upload = MultipartUpload.objects.get(id=request.data['id'])
        if multipart_upload.r2_file.metadata.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        complete_multipart_upload(multipart_upload)
        multipart_upload.r2_file.upload_completed = True
        multipart_upload.r2_file.save()
        multipart_upload.completed = True
        multipart_upload.save()
        return Response(status=status.HTTP_200_OK)

    