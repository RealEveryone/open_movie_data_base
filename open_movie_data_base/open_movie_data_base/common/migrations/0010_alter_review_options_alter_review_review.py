# Generated by Django 4.1.3 on 2022-12-05 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_reviewlike'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-posted_on']},
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(max_length=600),
        ),
    ]