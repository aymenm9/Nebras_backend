from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Profile

@receiver(pre_delete, sender=Profile)
def profile_delete(sender, instance, **kwargs):
    if instance.profile_image:
        instance.profile_image.delete(save=False)


def create_default_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    from decouple import config

    User = get_user_model()

    if User.objects.filter(is_superuser=True).exists():
        return

    username = config('ADMIN_USERNAME', default='admin')
    password = config('ADMIN_PASSWORD', default='admin')
    email = config('ADMIN_EMAIL', default='admin@nebras.com')

    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"[Nebras] Default superuser '{username}' created successfully.")
