from rest_framework import generics
from users.permissions import IsModerator
from .models import MainSection, SubSection, SecondarySubSection
from .serializers import MainSectionSerializer, SubSectionSerializer, SecondarySubSectionSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

class MainSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Main Sections (Moderators only).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by']
    search_fields = ['name']

    def get_queryset(self):
        return MainSection.objects.all().filter(created_by=self.request.user)

class MainSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Main Section (Super Admin only).
    """
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]

    def get_queryset(self):
        return MainSection.objects.all().filter(created_by=self.request.user)

class SubSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Sub Sections (Moderators only).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','main_section']
    search_fields = ['name']

    def get_queryset(self):
        return SubSection.objects.all().filter(created_by=self.request.user)

class SubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Sub Section (Moderators only).
    """
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]


    def get_queryset(self):
        return SubSection.objects.all().filter(created_by=self.request.user)

class SecondarySubSectionListCreateView(generics.ListCreateAPIView):
    """
    List and create Secondary Sub Sections (Moderators only).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['created_by','sub_section','sub_section__main_section']
    search_fields = ['name']

    def get_queryset(self):
        return SecondarySubSection.objects.all().filter(created_by=self.request.user)

class SecondarySubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Secondary Sub Section (Moderators only).
    """
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsAuthenticated,IsModerator]

    def get_queryset(self):
        return SecondarySubSection.objects.all().filter(created_by=self.request.user)

