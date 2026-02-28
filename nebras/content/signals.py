from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Metadata, R2File
from notifications.send import send_message
from notifications.models import Device
from .utils import abort_s3_multipart_upload, delete_s3_object

@receiver(post_save, sender=Metadata)
def send_notification(sender, instance, **kwargs):
    for device in Device.objects.filter(is_active=True):
        send_message(device, f"new content on nebras", f"{instance.title} has been added to nebras library")

@receiver(pre_delete, sender=R2File)
def r2file_pre_delete(sender, instance, **kwargs):
    if instance.upload_type == 'multipart':
        if instance.upload_status != 'completed' and hasattr(instance, 'multipart_uploader') and instance.multipart_uploader.upload_id:
            abort_s3_multipart_upload(instance.file_key, instance.multipart_uploader.upload_id)
        else:
            delete_s3_object(instance.file_key)
    else:
        delete_s3_object(instance.file_key)

@receiver(post_delete, sender=R2File)
def r2file_post_delete(sender, instance, **kwargs):
    # Ensure metadata is cleaned up when R2File is deleted.
    # We use post_delete so we don't accidentally delete the metadata if the R2File deletion fails.
    if hasattr(instance, 'metadata') and instance.metadata:
        instance.metadata.delete()