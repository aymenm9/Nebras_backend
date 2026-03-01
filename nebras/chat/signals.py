from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MessageFile

@receiver(pre_delete, sender=MessageFile)
def message_file_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
