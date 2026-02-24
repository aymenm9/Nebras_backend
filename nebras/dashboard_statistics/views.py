from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator

from content.models import Metadata, YoutubeVideo
from sections.models import MainSection, SubSection, SecondarySubSection
from .serializers import (
    TotalsSerializer, ContentDistributionSerializer, 
    ContentAddedChartSerializer
)

class ModeratorTotalsView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        user = request.user
        total_content_items = Metadata.objects.filter(created_by=user).count()
        total_youtube_videos = YoutubeVideo.objects.filter(metadata__created_by=user).count()
        
        total_main_sections = MainSection.objects.filter(created_by=user).count()
        total_sub_sections = SubSection.objects.filter(created_by=user).count()
        total_secondary_sections = SecondarySubSection.objects.filter(created_by=user).count()
        total_sections = total_main_sections + total_sub_sections + total_secondary_sections

        data = {
            'total_content_items': total_content_items,
            'total_youtube_videos': total_youtube_videos,
            'total_sections': total_sections,
        }
        serializer = TotalsSerializer(data)
        return Response(serializer.data)

class ModeratorContentDistributionView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        distribution = Metadata.objects.filter(created_by=request.user).values('content_type').annotate(count=Count('id'))
        
        data = {'video': 0, 'audio': 0, 'document': 0, 'youtube': 0}
        for item in distribution:
            if item['content_type'] in data:
                data[item['content_type']] = item['count']
                
        serializer = ContentDistributionSerializer(data)
        return Response(serializer.data)

class ModeratorContentAddedChartView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        content_added = Metadata.objects.filter(created_by=request.user, created_at__gte=thirty_days_ago) \
            .annotate(date=TruncDate('created_at')) \
            .values('date', 'content_type') \
            .annotate(count=Count('id')) \
            .order_by('date')
            
        data = {'data': list(content_added)}
        serializer = ContentAddedChartSerializer(data)
        return Response(serializer.data)
