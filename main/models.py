from django.db import models
from django.core.validators import (
    MinValueValidator,
)
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(
            default=1, 
            validators=[
                MinValueValidator(1),
            ]
    )
    comment = models.ManyToManyField("Comment")
    # TODO
    # Need to add one to many field so we can have on_delete

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