from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Metadata, R2File, YoutubeVideo
from notifications.send import send_message
from notifications.models import Device
from .utils import abort_s3_multipart_upload, delete_s3_object
from firebase_admin.messaging import Message
from firebase_admin.exceptions import FirebaseError
from notifications.tasks import send_bulk_notification

@receiver(post_save, sender=YoutubeVideo)
def send_notification_youtube_video(sender, instance, **kwargs):
    for device in Device.objects.filter(is_active=True):
        message = messaging.Message(
        token=device.token,
        notification=messaging.Notification(
            title="New Content",
            body="Check the new video"
        ),
        data={
            "title_en": "New Content",
            "body_en": "Check the new video",
            "title_ar": "محتوى جديد",
            "body_ar": "تحقق من الفيديو الجديد",
            "type": "youtube_video",
            "id": instance.id,
            "content_title": instance.metadata.title,
            "content_description": instance.metadata.description,
            "content_type": "youtube_video"
        }
    )
        send_message(device, message)

@receiver(post_save, sender=R2File)
def send_notification_r2file(sender, instance, **kwargs):
    for device in Device.objects.filter(is_active=True):
        message = messaging.Message(
        token=device.token,
        notification=messaging.Notification(
            title="New Content",
            body="Check the new content"
        ),
        data={
            "title_en": "New Content",
            "body_en": "Check the new content",
            "title_ar": "محتوى جديد",
            "body_ar": "تحقق من المحتوى الجديد",
            "type": "r2_file",
            "id": instance.id,
            "content_title": instance.metadata.title,
            "content_description": instance.metadata.description,
            "content_type": "r2_file"
        }
    )
        send_message(device, message)

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

@receiver(pre_delete, sender=Metadata)
def metadata_pre_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)