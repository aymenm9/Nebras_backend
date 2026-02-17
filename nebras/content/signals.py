from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Metadata
from notifications.send import send_message

@receiver(post_save, sender=Metadata)
def send_notification(sender, instance, **kwargs):
    if instance.created_by:
        send_message(instance.created_by, f"new content on nebras", f"{instance.title} has been added to nebras library")