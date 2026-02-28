from rest_framework import serializers
from .models import Metadata, YoutubeVideo, R2File, MultipartUpload, Part
from .utils import generate_presigned_url, create_file_key, create_multipart_upload, clc_total_parts, complete_multipart_upload
from django.conf import settings
class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'id', 'author']

    
class YoutubeVideoSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer()
    thumbnail = serializers.ImageField(required=False)
    class Meta:
        model = YoutubeVideo
        fields = ['id', 'video_url', 'metadata', 'thumbnail']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        metadata_data.pop('thumbnail', None)
        thumbnail = validated_data.pop('thumbnail', None)
        metadata_data.pop('content_type')
        user = self.context['request'].user
        metadata_instance = Metadata.objects.create(created_by=user, content_type='youtube', thumbnail=thumbnail, **metadata_data)
        youtube_video = YoutubeVideo.objects.create(metadata=metadata_instance, **validated_data)
        return youtube_video


class MultipartUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipartUpload
        fields = ['id','total_parts', 'uploaded_parts', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'uploaded_parts', 'total_parts', 'id', 'upload_id']


class R2FileSerializer(serializers.ModelSerializer):
    # this will be use only to create a new R2File instance no upload logic hire will be in separated serializer and view 
    metadata = MetadataSerializer()
    file_url = serializers.SerializerMethodField(read_only=True) # the read url only not the presigned url for upload 
    multipart_uploader = MultipartUploadSerializer(read_only=True)
    thumbnail = serializers.ImageField(required=False)
    
    class Meta:
        model = R2File
        fields = ['id', 'file_url', 'metadata', 'filename', 'file_size', 'file_type', 'upload_status', 'upload_type', 'multipart_uploader', 'thumbnail']
        read_only_fields = ['file_url', 'file_key', 'created_at', 'updated_at', 'id', 'upload_status', 'upload_type', 'multipart_uploader']

    def get_file_url(self, obj):
        if obj.upload_status == 'completed':
            if getattr(settings, 'R2_PUBLIC_DOMAIN', None):
                return f"{settings.R2_PUBLIC_DOMAIN.rstrip('/')}/{obj.file_key}"
            return generate_presigned_url(obj, method='get_object')
        return None
        
    def create(self, validated_data):
        thumbnail = validated_data.pop('thumbnail', None)
        # create the metadata first
        metadata_data = validated_data.pop('metadata')
        metadata_data.pop('thumbnail', None)
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
        validated_data['upload_status'] = 'pending'
        if file_type:
            content_type = 'document' if file_type.startswith('application/') else 'audio' if file_type.startswith('audio/') else 'video'
            metadata_data.pop('content_type', None)
        else:
            content_type = metadata_data.pop('content_type', 'document')
        
        metadata_instance = Metadata.objects.create(created_by=created_by, content_type=content_type, thumbnail=thumbnail, **metadata_data)
        if validated_data.get('file_size') > settings.MULTIPART_THRESHOLD: # 5MB
            # create a multipart upload and upload_type to multipart 
            validated_data['upload_type'] = 'multipart'
            r2_file = R2File.objects.create(metadata=metadata_instance, **validated_data)
            upload_id = create_multipart_upload(r2_file)
            total_parts = clc_total_parts(r2_file.file_size)
            multipart_upload = MultipartUpload.objects.create(r2_file=r2_file, upload_id=upload_id, total_parts=total_parts)
        else:
            validated_data['upload_type'] = 'single'
            r2_file = R2File.objects.create(metadata=metadata_instance, **validated_data)
        return r2_file
        


class PartSerializer(serializers.ModelSerializer):
    # this will only be response for the creattion of a new part not for get next part to upload or complet the upload
    class Meta:
        model = Part
        fields = ['id', 'multipart_upload', 'part_number', 'etag', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'id']

    def create(self, validated_data):
        # if the part allready exist keep the new one etag and completed
        if Part.objects.filter(multipart_upload=validated_data['multipart_upload'], part_number=validated_data['part_number']).exists():
            part = Part.objects.get(multipart_upload=validated_data['multipart_upload'], part_number=validated_data['part_number'])
            part.etag = validated_data['etag']
            part.completed = validated_data.get('completed', True)
            part.save()
            return part
        multipart_upload = validated_data.pop('multipart_upload')
        validated_data['completed'] = True
        part = Part.objects.create(multipart_upload=multipart_upload, **validated_data)
        part.multipart_upload.uploaded_parts += 1
        part.multipart_upload.save()
        return part
    
    def update(self, instance, validated_data):
        instance.part_number = validated_data.get('part_number', instance.part_number)
        instance.etag = validated_data.get('etag', instance.etag)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
    

class MultipartUploadResponseSerializer(serializers.Serializer):
    presigned_url = serializers.URLField()
    next_part_number = serializers.IntegerField()

class SimpleUploadResponseSerializer(serializers.Serializer):
    presigned_url = serializers.URLField()


class AllContentSerializer(serializers.ModelSerializer):
    youtube_video = YoutubeVideoSerializer(required=False, allow_null=True)
    r2_file = R2FileSerializer(required=False, allow_null=True)
    class Meta:
        model = Metadata
        fields = ['id', 'title', 'description', 'content_type', 'subsection', 'secondary_subsection', 'created_by', 'created_at', 'updated_at', 'youtube_video', 'r2_file', 'author', 'thumbnail']
        read_only_fields = ['created_at', 'updated_at', 'id', 'author', 'created_by', 'thumbnail', 'content_type', 'subsection', 'secondary_subsection', 'is_listed']

    