# Generated by Django 4.1.3 on 2022-11-30 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_alter_movie_slug'),
        ('common', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(max_length=300),
        ),
        migrations.CreateModel(
            name='AverageReviewScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
        ),
    ]