# Generated by Django 4.1.3 on 2022-12-18 09:04

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_alter_moviegenres_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_poster',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]