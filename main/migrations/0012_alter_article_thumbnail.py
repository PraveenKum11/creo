# Generated by Django 4.1.3 on 2022-12-31 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_article_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="thumbnail",
            field=models.ImageField(upload_to="article_img"),
        ),
    ]
