from rest_framework import generics
from users.permissions import IsModerator
from .models import MainSection, SubSection, SecondarySubSection
from .serializers import MainSectionSerializer, SubSectionSerializer, SecondarySubSectionSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class MainSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Main Sections (Moderators only).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by']
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MainSection.objects.all()
        return MainSection.objects.all().filter(created_by=self.request.user)

class MainSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Main Section (Super Admin only).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsModerator]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MainSection.objects.all()
        return MainSection.objects.all().filter(created_by=self.request.user)

class SubSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Sub Sections (Moderators only).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','main_section']
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SubSection.objects.all()
        return SubSection.objects.all().filter(created_by=self.request.user)

class SubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Sub Section (Moderators only).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsModerator]


    def get_queryset(self):
        if self.request.user.is_superuser:
            return SubSection.objects.all()
        return SubSection.objects.all().filter(created_by=self.request.user)

class SecondarySubSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Secondary Sub Sections (Moderators only).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','sub_section','sub_section__main_section']
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SecondarySubSection.objects.all()
        return SecondarySubSection.objects.all().filter(created_by=self.request.user)

class SecondarySubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Secondary Sub Section (Moderators only).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsModerator]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SecondarySubSection.objects.all()
        return SecondarySubSection.objects.all().filter(created_by=self.request.user)

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
