# Generated by Django 4.2.6 on 2023-12-10 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_userchallenge_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchallenge',
            name='progress',
        ),
        migrations.AddField(
            model_name='reward',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]
