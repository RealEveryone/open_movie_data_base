# Generated by Django 4.1.3 on 2022-12-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='averagereviewscore',
            name='total_sum_of_numbers',
            field=models.FloatField(default=0),
        ),
    ]