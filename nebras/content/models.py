from django.db import models
from django.contrib.auth.models import User
from sections.models import SubSection, SecondarySubSection
from storages.backends.s3boto3 import S3Boto3Storage
# Create your models here.


class Metadata(models.Model):
    title = models.CharField(max_length=512)
    content_type = models.CharField(choices=[
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('youtube', 'Youtube'),
    ])
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='content/thumbnails', 
        storage=S3Boto3Storage(), 
        null=True, 
        blank=True
    )
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE)
    secondary_subsection = models.ForeignKey(SecondarySubSection, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class YoutubeVideo(models.Model):
    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE, related_name='youtube_video')
    video_url = models.CharField(max_length=512)
    

class R2File(models.Model):

    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE, related_name='r2_file')
    file_key = models.CharField(max_length=512) # Path in R2 and url in youtube
    filename = models.CharField(max_length=512, null=True, blank=True)# file name UID 
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)# actual file type like video/mp4 or audio/mpeg, application/pdf for the R2 files
    upload_status = models.CharField(max_length=100, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    upload_type = models.CharField(max_length=100, choices=[
        ('single', 'Single'),
        ('multipart', 'Multipart'),
    ], default='single')
    def __str__(self):
        return f'{self.metadata.title}'

class MultipartUpload(models.Model):
    r2_file = models.OneToOneField(R2File, on_delete=models.CASCADE, related_name='multipart_uploader')
    upload_id = models.CharField(max_length=100, null=True, blank=True) # upload id for multipart upload
    completed = models.BooleanField(default=False)
    total_parts = models.IntegerField()
    uploaded_parts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.r2_file.metadata.title}'

class Part(models.Model):
    multipart_upload = models.ForeignKey(MultipartUpload, on_delete=models.CASCADE, related_name='parts')
    part_number = models.IntegerField()
    etag = models.CharField(max_length=100, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['multipart_upload', 'part_number']]
        indexes = [
            models.Index(fields=['multipart_upload', 'part_number']),
        ]
    
    def __str__(self):
        return f'Part {self.part_number}/{self.multipart_upload.total_parts} - {self.multipart_upload.r2_file.metadata.title}'
    