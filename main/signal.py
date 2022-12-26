from django.db.models.signals import (
    post_save,
)
from django.contrib.auth.models import User
from django.dispatch import receiver
from main import models

from PIL import Image

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = models.Profile.objects.create(user=instance)

        image = Image.open(r"C:\Users\pkkp0\Documents\pydev\web_dev\blog_web\static\main\media\img5.jpg")
        output_size = (300, 300)
        if image.height > 300 or image.width > 300:
            image.thumbnail(output_size)
        image.save(profile.img.path)
