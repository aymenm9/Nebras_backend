from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Metadata
from notifications.send import send_message
from notifications.models import Device

@receiver(post_save, sender=Metadata)
def send_notification(sender, instance, **kwargs):
    for device in Device.objects.filter(is_active=True):
        send_message(device, f"new content on nebras", f"{instance.title} has been added to nebras library")