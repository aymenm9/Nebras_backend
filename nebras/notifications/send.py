from .models import Device
from . import firebase
from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError


def send_message(device: Device, title:str, body:str):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=device.token,
        )
        messaging.send(message)
    except FirebaseError as e:
        device.is_active = False
        device.save()
