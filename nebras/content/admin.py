from django.contrib import admin
from .models import Metadata, YoutubeVideo, R2File, Part, MultipartUpload

@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_type', 'subsection', 'created_by', 'created_at')
    list_filter = ('content_type', 'subsection', 'created_by')
    search_fields = ('title', 'description')

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'metadata', 'video_url')

@admin.register(R2File)
class R2FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'metadata', 'file_type', 'file_size', 'upload_status')
    list_filter = ('upload_status', 'file_type')

@admin.register(MultipartUpload)
class MultipartUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'r2_file', 'upload_id', 'created_at', 'completed', 'total_parts', 'uploaded_parts')
    list_filter = ('created_at',)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'multipart_upload', 'part_number', 'etag', 'completed')
    list_filter = ('multipart_upload','completed')
