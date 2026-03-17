from django_huey import task
from .send import send_message
from firebase_admin.messaging import Message

@task()
def send_notification(device_token: str, message:Message):
    send_message(device_token, message)


@task()
def send_bulk_notification(device_tokens: list[str], message:Message):
    for device_token in device_tokens:
        send_message(device_token, message)


