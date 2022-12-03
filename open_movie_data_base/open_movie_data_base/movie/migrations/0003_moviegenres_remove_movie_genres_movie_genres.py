# Generated by Django 4.1.3 on 2022-11-25 07:06

from django.db import migrations, models
import open_movie_data_base.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieGenres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, validators=[open_movie_data_base.utils.validators.CharValidator('^[A-Za-z\\w-]+\\Z', 'Use only latin letters, spaces and dashes')])),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='movie.moviegenres'),
        ),
    ]
