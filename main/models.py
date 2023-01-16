from django.db import models
from django.core.validators import (
    MinValueValidator,
)
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from PIL import Image

class Article(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="article_img", blank=True)

    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    comment = models.ManyToManyField("Comment", blank=True)

    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=256)
    comment_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.commentor)

class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(max_length=250 ,default="default.jpg", upload_to="profile_pics")
    location = models.CharField(max_length=50, default="Earth", blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    # Overriding the save method of model
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.img.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.img.path)

    def __str__(self):
        return f"{self.user.username} Profile"