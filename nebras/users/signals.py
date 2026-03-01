from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Profile

@receiver(pre_delete, sender=Profile)
def profile_delete(sender, instance, **kwargs):
    if instance.profile_image:
        instance.profile_image.delete(save=False)
