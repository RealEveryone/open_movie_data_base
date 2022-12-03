# Generated by Django 4.1.3 on 2022-11-24 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(to='user.actor'),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.moviedirector'),
        ),
    ]
