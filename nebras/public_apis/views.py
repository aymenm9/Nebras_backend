from rest_framework import generics
from sections.models import MainSection, SubSection, SecondarySubSection
from sections.serializers import MainSectionSerializer, SubSectionSerializer, SecondarySubSectionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from content.models import YoutubeVideo, Metadata, R2File
from content.serializers import YoutubeVideoSerializer, MetadataSerializer, R2FileSerializer

class PublicMainSectionListView(generics.ListAPIView):
    """
    Public list of Main Sections (No Auth).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by']
    search_fields = ['name']


class PublicMainSectionRetrieveView(generics.RetrieveAPIView):
    """
    Public retrieve of Main Section (No Auth).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer


class PublicSubSectionListView(generics.ListAPIView):
    """
    Public list of Sub Sections (No Auth).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','main_section']
    search_fields = ['name']


class PublicSubSectionRetrieveView(generics.RetrieveAPIView):
    """
    Public retrieve of Sub Section (No Auth).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer


class PublicSecondarySubSectionListView(generics.ListAPIView):
    """
    Public list of Secondary Sub Sections (No Auth).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','sub_section','sub_section__main_section']
    search_fields = ['name']

class PublicSecondarySubSectionRetrieveView(generics.RetrieveAPIView):
    """
    Public retrieve of Secondary Sub Section (No Auth).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer


class PublishYoutubeVideo(generics.ListAPIView):
    serializer_class = YoutubeVideoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type']
    search_fields = ['metadata__title','metadata__description']
    queryset = YoutubeVideo.objects.all()

class PublishYoutubeVideoDetail(generics.RetrieveAPIView):
    serializer_class = YoutubeVideoSerializer
    queryset = YoutubeVideo.objects.all()

class PublishMetadata(generics.ListAPIView):
    serializer_class = MetadataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','subsection','subsection__main_section','secondary_subsection','content_type']
    search_fields = ['title','description']
    queryset = Metadata.objects.all()

class PublishMetadataDetail(generics.RetrieveAPIView):
    serializer_class = MetadataSerializer
    queryset = Metadata.objects.all()

class PublishR2File(generics.ListAPIView):
    serializer_class = R2FileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['metadata__created_by','metadata__subsection','metadata__subsection__main_section','metadata__secondary_subsection','metadata__content_type']
    search_fields = ['metadata__title','metadata__description']
    queryset = R2File.objects.all().filter(upload_completed=True)

class PublishR2FileDetail(generics.RetrieveAPIView):
    serializer_class = R2FileSerializer
    queryset = R2File.objects.all().filter(upload_completed=True)