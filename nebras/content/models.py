from django.db import models
from django.contrib.auth.models import User
from sections.models import SubSection, SecondarySubSection
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
    thumbnail = models.ImageField(upload_to='content/thumbnails',null=True, blank=True)
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
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=100, null=True, blank=True)# actual file type like video/mp4 or audio/mpeg, application/pdf for the R2 files
    upload_completed = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.metadata.title}'
    