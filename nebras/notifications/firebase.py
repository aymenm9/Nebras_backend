import firebase_admin
from firebase_admin import credentials
from django.conf import settings
import os

if not firebase_admin._apps:
    cred = credentials.Certificate(
        os.path.join(settings.BASE_DIR, "nebras-3ae62-firebase-adminsdk-fbsvc-3a5a764db7.json")
    )
    firebase_admin.initialize_app(cred)
