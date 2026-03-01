from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='public/profiles/images/', 
        storage=S3Boto3Storage(), 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bans')
    reason = models.TextField(null=True, blank=True)
    banned_start = models.DateTimeField(auto_now_add=True)
    banned_end = models.DateTimeField()
    banned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banned_by')
    is_banned = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s Ban"