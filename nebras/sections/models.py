from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

class MainSection(models.Model):
    name = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='public/section_thumbnails', storage=S3Boto3Storage(), blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return self.name

class SubSection(models.Model):
    main_section = models.ForeignKey(MainSection, on_delete=models.CASCADE, related_name='sub_sections')
    name = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='public/sub_section_thumbnails', storage=S3Boto3Storage(), blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return f"{self.main_section.name} -> {self.name}"

class SecondarySubSection(models.Model):
    main_section = models.ForeignKey(MainSection, on_delete=models.CASCADE, related_name='secondary_sections')
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='secondary_sub_sections')
    name = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='public/secondary_section_thumbnails', storage=S3Boto3Storage(), blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return f"{self.sub_section.name} -> {self.name}"
