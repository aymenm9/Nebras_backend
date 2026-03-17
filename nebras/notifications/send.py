from .models import Device
from . import firebase
from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError


def send_message(device: Device, message:messaging.Message):
    try:
        messaging.send(message)
    except FirebaseError as e:
        device.is_active = False
        device.save()
