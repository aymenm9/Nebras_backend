from rest_framework import serializers
from .models import Metadata, YoutubeVideo, R2File
from .utils import generate_presigned_url, create_file_key

class MetadataSerializerUpload(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
class YoutubeVideoSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializerUpload()
    class Meta:
        model = YoutubeVideo
        fields = ['id', 'video_url', 'metadata']
        
    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        user = self.context['request'].user
        metadata_instance = Metadata.objects.create(created_by=user, **metadata_data)
        youtube_video = YoutubeVideo.objects.create(metadata=metadata_instance, **validated_data)
        return youtube_video

class R2FileSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializerUpload(source='metadata')
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = R2File
        fields = '__all__'
        read_only_fields = ['file_url', 'file_key']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='get')
    

class R2FileSerializerUpload(serializers.ModelSerializer):
    metadata = MetadataSerializerUpload(source='metadata')
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = R2File
        fields = '__all__'
        read_only_fields = ['file_url', 'file_key']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='put')

    
    def create(self, validated_data):
        metadata_data = validated_data.get('metadata')
        section = metadata_data.get('subsection')
        subsection = metadata_data.get('subsection')
        secondary_subsection = metadata_data.get('secondary_subsection')
        file_type = metadata_data.get('content_type')
        file_key = create_file_key(section.name, subsection.name, secondary_subsection.name if secondary_subsection else None, file_type)
        validated_data['file_key'] = file_key
        validated_data['created_by'] = self.context['request'].user
        validated_data['upload_completed'] = False
        return super().create(validated_data)
        