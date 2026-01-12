from rest_framework import serializers
from .models import Metadata, YoutubeVideo, R2File
from .utils import generate_presigned_url, create_file_key

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    
class YoutubeVideoSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer()
    class Meta:
        model = YoutubeVideo
        fields = ['id', 'video_url', 'metadata']
        
    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        metadata_data.pop('content_type')
        user = self.context['request'].user
        metadata_instance = Metadata.objects.create(created_by=user, content_type='youtube',**metadata_data)
        youtube_video = YoutubeVideo.objects.create(metadata=metadata_instance, **validated_data)
        return youtube_video

class R2FileSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = R2File
        fields = ['id', 'file_url', 'metadata', 'filename', 'file_size', 'file_type', 'upload_completed']
        read_only_fields = ['file_url', 'file_key', 'created_by', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='get')
    

class R2FileSerializerUpload(serializers.ModelSerializer):
    metadata = MetadataSerializer()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = R2File
        fields = ['id', 'file_url', 'metadata', 'filename', 'file_size', 'file_type']
        read_only_fields = ['file_url', 'file_key', 'created_by', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='put')

    
    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        secondary_subsection = metadata_data.get('secondary_subsection')
        if not secondary_subsection:
            subsection = metadata_data.get('subsection')
            section = subsection.main_section
        else:
            subsection = secondary_subsection.sub_section
            section = subsection.main_section

        file_type = validated_data.get('file_type',None)
        file_key = create_file_key(section.name, subsection.name, secondary_subsection.name if secondary_subsection else None, file_type)
        validated_data['file_key'] = file_key
        created_by = self.context['request'].user
        validated_data['upload_completed'] = False
        if file_type:
            content_type = 'document' if file_type.startswith('application/') else 'audio' if file_type.startswith('audio/') else 'video'
            metadata_data.pop('content_type', None)
        else:
            content_type = metadata_data.pop('content_type', 'document')
        
        metadata_instance = Metadata.objects.create(created_by=created_by, content_type=content_type, **metadata_data)
        r2_file = R2File.objects.create(metadata=metadata_instance, **validated_data)
        return r2_file
        
