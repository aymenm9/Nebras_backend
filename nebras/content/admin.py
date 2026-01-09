from django.contrib import admin
from .models import Metadata, YoutubeVideo, R2File

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
    list_display = ('id', 'metadata', 'file_type', 'file_size', 'upload_completed')
    list_filter = ('upload_completed', 'file_type')
