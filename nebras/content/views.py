from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Metadata, YoutubeVideo, R2File
from .serializers import MetadataSerializer, YoutubeVideoSerializer, R2FileSerializer, R2FileSerializerUpload
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
        if self.request.user.is_superuser:
            return YoutubeVideo.objects.all()
        return YoutubeVideo.objects.filter(metadata__created_by=self.request.user)

class UploadYoutubeVideoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = YoutubeVideoSerializer
    queryset = YoutubeVideo.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return YoutubeVideo.objects.all()
        return YoutubeVideo.objects.filter(metadata__created_by=self.request.user)


class R2FileUpload(generics.ListAPIView):
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type']
    search_fields = ['metadata__title','metadata__description']
    queryset = R2File.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return R2File.objects.all()
        return R2File.objects.filter(created_by=self.request.user)

class R2FileUploadCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = R2FileSerializerUpload
    


class R2FileUploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsModerator]
    serializer_class = R2FileSerializer
    queryset = R2File.objects.all().filter(upload_completed=True)
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return R2File.objects.all()
        return R2File.objects.filter(created_by=self.request.user)

