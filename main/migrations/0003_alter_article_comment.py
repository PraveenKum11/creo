# Generated by Django 4.1.3 on 2022-12-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_comment_commentor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="comment",
            field=models.ManyToManyField(blank=True, to="main.comment"),
        ),
    ]
