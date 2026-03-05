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

from chat.models import ChatMessage, MessageFile
from chat.serializers import ChatMessageSerializer, MessageFileSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from content.models import Metadata
from dashboard_statistics.serializers import (
    TotalsSerializer, ContentDistributionSerializer, 
    TopSectionsSerializer, RegistrationsChartSerializer, 
    ContentAddedChartSerializer
)
from drf_spectacular.utils import extend_schema
# Moderator Management (Moderators are super admin only)
class AdminModeratorListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    serializer_class = ModeratorSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['is_staff', 'is_active']
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
    filterset_fields = ['created_by','is_listed']
    search_fields = ['name']

class AdminMainSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MainSection.objects.all()
    serializer_class = MainSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminSubSectionListView(generics.ListAPIView):
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['created_by', 'main_section','is_listed']
    search_fields = ['name']

class AdminSubSectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubSection.objects.all()
    serializer_class = SubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminSecondarySubSectionListView(generics.ListAPIView):
    queryset = SecondarySubSection.objects.all()
    serializer_class = SecondarySubSectionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['created_by', 'sub_section', 'sub_section__main_section','is_listed']
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
    filterset_fields = ['metadata__created_by', 'metadata__subsection', 'metadata__subsection__main_section', 'metadata__content_type','metadata__is_listed']
    search_fields = ['metadata__title', 'metadata__description','metadata__author']

class AdminYoutubeVideoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = YoutubeVideo.objects.all()
    serializer_class = YoutubeVideoSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminR2FileListView(generics.ListAPIView):
    queryset = R2File.objects.all()
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['metadata__created_by', 'metadata__subsection', 'metadata__subsection__main_section', 'metadata__content_type','metadata__is_listed']
    search_fields = ['metadata__title', 'metadata__description','metadata__author']

class AdminR2FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = R2File.objects.all()
    serializer_class = R2FileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

# Chat Management (Super Admin only view and manage all chat logs)
class AdminChatMessageListView(generics.ListAPIView):
    queryset = ChatMessage.objects.all().order_by('-created_at')
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['user']
    search_fields = ['message', 'user__username', 'user__email']

class AdminChatMessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class AdminMessageFileListView(generics.ListAPIView):
    queryset = MessageFile.objects.all()
    serializer_class = MessageFileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filterset_fields = ['user', 'message']

class AdminMessageFileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MessageFile.objects.all()
    serializer_class = MessageFileSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

# Statistics Views



class AdminTotalsView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        description="Get the total counts of various entities in the system.",
        responses=TotalsSerializer
    )
    def get(self, request):
        total_moderators = User.objects.filter(is_staff=True, is_superuser=False).count()
        total_content_items = Metadata.objects.count()
        total_main_sections = MainSection.objects.count()
        total_sub_sections = SubSection.objects.count()
        total_secondary_sections = SecondarySubSection.objects.count()
        total_sections = total_main_sections + total_sub_sections + total_secondary_sections
        total_chat_queries = ChatMessage.objects.count()

        data = {
            'total_moderators': total_moderators,
            'total_content_items': total_content_items,
            'total_main_sections': total_main_sections,
            'total_sub_sections': total_sub_sections,
            'total_secondary_sections': total_secondary_sections,
            'total_sections': total_sections,
            'total_chat_queries': total_chat_queries,
        }
        serializer = TotalsSerializer(data)
        return Response(serializer.data)

class AdminContentDistributionView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        description="Get the distribution of content items by content type.",
        responses=ContentDistributionSerializer
    )
    def get(self, request):
        distribution = Metadata.objects.values('content_type').annotate(count=Count('id'))
        
        data = {'video': 0, 'audio': 0, 'document': 0, 'youtube': 0}
        for item in distribution:
            if item['content_type'] in data:
                data[item['content_type']] = item['count']
                
        serializer = ContentDistributionSerializer(data)
        return Response(serializer.data)

class AdminTopSectionsView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        description="Get the top sections based on the number of content items.",
        responses=TopSectionsSerializer(many=True)
    )
    def get(self, request):
        # Annotate main_sections with the total count of their nested subsections metadata
        top_sections = MainSection.objects.annotate(
            content_count=Count('sub_sections__metadata') + Count('sub_sections__secondary_sub_sections__metadata')
        ).order_by('-content_count')[:10]
        
        data = [
            {'id': section.id, 'name': section.name, 'content_count': section.content_count}
            for section in top_sections
        ]
        serializer = TopSectionsSerializer(data, many=True)
        return Response(serializer.data)

class AdminRegistrationsChartView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        description="Get the number of user registrations in the last 30 days, grouped by date.",
        responses=RegistrationsChartSerializer(many=True)
    )
    def get(self, request):
        
        registrations = User.objects.annotate(date=TruncDate('date_joined')) \
            .values('date') \
            .annotate(count=Count('id')) \
            .order_by('date')
            
        data = {'data': list(registrations)}
        serializer = RegistrationsChartSerializer(data)
        return Response(serializer.data)

class AdminContentAddedChartView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        description="Get the number of content items added in the last 30 days, grouped by date and content type.",
        responses=ContentAddedChartSerializer(many=True)
    )
    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        content_added = Metadata.objects.filter(created_at__gte=thirty_days_ago) \
            .annotate(date=TruncDate('created_at')) \
            .values('date', 'content_type') \
            .annotate(count=Count('id')) \
            .order_by('date')
            
        data = {'data': list(content_added)}
        serializer = ContentAddedChartSerializer(data)
        return Response(serializer.data)
