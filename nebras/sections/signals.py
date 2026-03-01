from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MainSection, SubSection, SecondarySubSection

@receiver(pre_delete, sender=MainSection)
def main_section_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)

@receiver(pre_delete, sender=SubSection)
def sub_section_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)

@receiver(pre_delete, sender=SecondarySubSection)
def secondary_sub_section_delete(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
