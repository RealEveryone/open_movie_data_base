# Generated by Django 4.1.3 on 2022-12-13 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averagereviewscore',
            name='score',
            field=models.FloatField(default=10),
        ),
    ]