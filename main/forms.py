from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from main import models

# Model forms
class Comment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("comment_content",)

class Article(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("title", "content", "tag")

class Profile(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ("first_name", "last_name", "email", "location", "hobbies")
