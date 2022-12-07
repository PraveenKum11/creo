from django import forms

from main import models

# Model forms
class Comment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("commentor", "comment_content")

class Article(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ("title", "content", "tag")

    # tag = forms.ModelChoiceField(queryset=models.Tag.objects, to_field_name="name")