from django.db.models.signals import (
    post_save,
)
from django.contrib.auth.models import User
from django.dispatch import receiver

from main import models
from main.management.commands.image_generator import Photo


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        img = Photo(type="Profile", query="nature")
        img_path = img.create_photo()
        models.Profile.objects.create(user=instance, img=img_path)