from django.db import models
from django.core.validators import (
    MinValueValidator,
)
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # thumbnail = models.ImageField(upload_to="images", blank=True)
    # TODO
    # Validator for image dimensitions

    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    comment = models.ManyToManyField("Comment", blank=True)

    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    commentor = models.CharField(max_length=50)
    comment_content = models.TextField(max_length=256)
    comment_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.commentor)

class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.name
