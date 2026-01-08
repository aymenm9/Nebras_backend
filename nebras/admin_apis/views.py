from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from users.models import Ban
from users.serializers import ModeratorSerializer, BanSerializer
from users.permissions import IsSuperAdmin

from sections.models import MainSection, SubSection, SecondarySubSection
from sections.serializers import MainSectionSerializer, SubSectionSerializer, SecondarySubSectionSerializer

from content.models import YoutubeVideo, R2File
from content.serializers import YoutubeVideoSerializer, R2FileSerializer

# Moderator Management (Moderators are super admin only)
class AdminModeratorListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    serializer_class = ModeratorSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

class AdminModeratorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    serializer_class = ModeratorSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

# Ban Management (Bans are super admin only)
class AdminBanUserView(generics.ListCreateAPIView):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['user', 'is_banned', 'banned_start', 'banned_end']
    search_fields = ['user__username', 'user__email', 'reason']

class AdminBanUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

# Section Management (Super Admin List/RUD Only - Creation via moderator APIs)
class AdminMainSectionListView(generics.ListAPIView):
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['created_by']
    search_fields = ['name']

class AdminMainSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminSubSectionListView(generics.ListAPIView):
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['created_by', 'main_section']
    search_fields = ['name']

class AdminSubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminSecondarySubSectionListView(generics.ListAPIView):
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['created_by', 'sub_section', 'sub_section__main_section']
    search_fields = ['name']

class AdminSecondarySubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

# Content Management (Super Admin List/RUD Only - Creation via moderator APIs)
class AdminYoutubeVideoListView(generics.ListAPIView):
    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubeVideoSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['metadata__created_by', 'metadata__subsection', 'metadata__subsection__main_section', 'metadata__content_type']
    search_fields = ['metadata__title', 'metadata__description']

class AdminYoutubeVideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubeVideoSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminR2FileListView(generics.ListAPIView):
    queryset = R2File.objects.all()
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['metadata__created_by', 'metadata__subsection', 'metadata__subsection__main_section', 'metadata__content_type']
    search_fields = ['metadata__title', 'metadata__description']

class AdminR2FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = R2File.objects.all()
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
