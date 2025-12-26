from django.db import models
from django.contrib.auth.models import User

class MainSection(models.Model):
    name = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return f"{self.main_section.name} -> {self.name}"

class SecondarySubSection(models.Model):
    sub_section = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='secondary_sub_sections')
    name = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']

    def __str__(self):
        return f"{self.sub_section.name} -> {self.name}"
