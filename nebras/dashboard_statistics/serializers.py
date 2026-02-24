from rest_framework import serializers

class TotalsSerializer(serializers.Serializer):
    total_moderators = serializers.IntegerField(required=False)
    total_content_items = serializers.IntegerField()
    total_main_sections = serializers.IntegerField(required=False)
    total_sub_sections = serializers.IntegerField(required=False)
    total_secondary_sections = serializers.IntegerField(required=False)
    total_sections = serializers.IntegerField(required=False)
    total_chat_queries = serializers.IntegerField(required=False)
    total_youtube_videos = serializers.IntegerField(required=False)

class ContentDistributionSerializer(serializers.Serializer):
    video = serializers.IntegerField(default=0)
    audio = serializers.IntegerField(default=0)
    document = serializers.IntegerField(default=0)
    youtube = serializers.IntegerField(default=0)

class TopSectionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    content_count = serializers.IntegerField()

class ChartDataPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

class RegistrationsChartSerializer(serializers.Serializer):
    data = ChartDataPointSerializer(many=True)

class ContentAddedChartDataPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    content_type = serializers.CharField()
    count = serializers.IntegerField()

class ContentAddedChartSerializer(serializers.Serializer):
    data = ContentAddedChartDataPointSerializer(many=True)
