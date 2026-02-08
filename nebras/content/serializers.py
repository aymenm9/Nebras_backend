from rest_framework import serializers
from .models import Metadata, YoutubeVideo, R2File, MultipartUpload, Part
from .utils import generate_presigned_url, create_file_key, create_multipart_upload, clc_total_parts, complete_multipart_upload
from django.conf.settings import MULTIPART_THRESHOLD
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
'''
class R2FileSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = R2File
        fields = ['id', 'file_url', 'metadata', 'filename', 'file_size', 'file_type', 'upload_completed']
        read_only_fields = ['file_url', 'file_key', 'created_by', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='get_object')
    
'''
class R2FileSerializer(serializers.ModelSerializer):
    # this will be use only to create a new R2File instance no upload logic hire will be in separated serializer and view 
    metadata = MetadataSerializer()
    file_url = serializers.SerializerMethodField(read_only=True) # the read url only not the presigned url for upload 
    
    class Meta:
        model = R2File
        fields = ['id', 'file_url', 'metadata', 'filename', 'file_size', 'file_type', 'upload_status', 'upload_type']
        read_only_fields = ['file_url', 'file_key', 'created_at', 'updated_at', 'id', 'upload_status', 'upload_type']

    def get_file_url(self, obj):
        return generate_presigned_url(obj, method='get_object') if obj.upload_status == 'completed' else None
        
    def create(self, validated_data):
        # create the metadata first
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
        if validated_data.get('file_size') > MULTIPART_THRESHOLD: # 5MB
            # create a multipart upload and upload_type to multipart 
            validated_data['upload_type'] = 'multipart'
            r2_file = R2File.objects.create(metadata=metadata_instance, **validated_data)
        return r2_file
        


class MultipartUploadSerializer(serializers.ModelSerializer):
    r2_file = R2FileSerializerUpload(write_only=True,required=False, allow_null=True)
    # if null the upload is complete 
    upload_url = serializers.SerializerMethodField(read_only=True,required=False, allow_null=True, source='get_upload_url')
    class Meta:
        model = MultipartUpload
        fields = ['id', 'r2_file', 'upload_url', 'total_parts', 'uploaded_parts', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'upload_url', 'uploaded_parts', 'total_parts', 'id', 'upload_id']

    def create(self, validated_data):
        r2_file = validated_data.pop('r2_file')
        # only the creat as i don't want to generate presigned url here & and the validation is already done in this serializer
        r2_file = R2FileSerializerUpload(context=self.context).create(r2_file) 
        upload_id = create_multipart_upload(r2_file)
        total_parts = clc_total_parts(r2_file.file_size)
        multipart_upload = MultipartUpload.objects.create(r2_file=r2_file, upload_id=upload_id, total_parts=total_parts, **validated_data)
        return multipart_upload
    
    def get_upload_url(self, obj):
        # get the last uploaded part number and add 1 to the next part number in case of retrive to complete the upload
        last_part = Part.objects.filter(multipart_upload=obj, completed=True).order_by('-part_number').first()
        if last_part:
            # if the last part is the last part return null
            if last_part.part_number == obj.total_parts:
                return None
            
            return generate_presigned_url(obj.r2_file, method='upload_part', part_number=last_part.part_number + 1, UploadId=obj.upload_id)
        return generate_presigned_url(obj.r2_file, method='upload_part', part_number=1, UploadId=obj.upload_id)

class PartSerializer(serializers.ModelSerializer):
    # get the presigned url for the next part to upload if null the upload is complete 
    upload_url = serializers.SerializerMethodField(read_only=True,required=False, allow_null=True, source='get_upload_url')
    class Meta:
        model = Part
        fields = ['id', 'multipart_upload', 'part_number', 'etag', 'completed', 'created_at', 'updated_at', 'upload_url']
        read_only_fields = ['created_at', 'updated_at', 'id', 'upload_url']

    def create(self, validated_data):
        multipart_upload = validated_data.pop('multipart_upload')
        part_number = validated_data.pop('part_number')
        etag = validated_data.pop('etag')
        validated_data.pop('completed')
        # completed=True ; as will create this obj after the user upload the part and get the ETag
        if Part.objects.filter(multipart_upload=multipart_upload, part_number=part_number).exists():
            raise serializers.ValidationError('Part already exists')
        part = Part.objects.create(multipart_upload=multipart_upload, part_number=part_number, etag=etag, completed=True, **validated_data)
        multipart_upload.uploaded_parts += 1
        multipart_upload.save()
        # complete the upload
        if part.part_number == part.multipart_upload.total_parts and Part.objects.filter(multipart_upload=part.multipart_upload, completed=True).count() == part.multipart_upload.total_parts:
            complete_multipart_upload(part.multipart_upload)
            part.multipart_upload.completed = True
            part.multipart_upload.save()
            part.multipart_upload.r2_file.upload_completed = True
            part.multipart_upload.r2_file.save()
            
        return part
    
    def update(self, instance, validated_data):
        instance.part_number = validated_data.get('part_number', instance.part_number)
        instance.etag = validated_data.get('etag', instance.etag)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance
    
    def get_upload_url(self, obj):
        # get the last uploaded part number and add 1 to the next part number in case of retrive to complete the upload
        
        part_n = obj.part_number + 1 if obj.part_number < obj.multipart_upload.total_parts else obj.part_number
        # if the last part is the last part return null
        return None if obj.part_number == obj.multipart_upload.total_parts else generate_presigned_url(obj.multipart_upload.r2_file, method='upload_part', part_number=part_n, UploadId=obj.multipart_upload.upload_id)
        