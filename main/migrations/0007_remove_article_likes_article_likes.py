# Generated by Django 4.1.3 on 2022-12-14 18:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0006_remove_article_comment_article_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="likes",
        ),
        migrations.AddField(
            model_name="article",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
