# Generated by Django 4.1.3 on 2022-12-05 08:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_alter_averagereviewscore_total_sum_of_numbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='posted_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
