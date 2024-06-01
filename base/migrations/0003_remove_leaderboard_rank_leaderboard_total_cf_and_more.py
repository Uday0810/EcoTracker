# Generated by Django 4.2.6 on 2023-12-07 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_carbonfootprint_educationalcontent_userprofile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderboard',
            name='rank',
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='total_cf',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twoWheeler', models.FloatField(default=0)),
                ('bus', models.FloatField(default=0)),
                ('car', models.FloatField(default=0)),
                ('trains', models.FloatField(default=0)),
                ('longHaulFlights', models.FloatField(default=0)),
                ('shortFlights', models.FloatField(default=0)),
                ('shortHaulFlights', models.FloatField(default=0)),
                ('ferry', models.FloatField(default=0)),
                ('naturalGas', models.FloatField(default=0)),
                ('coal', models.FloatField(default=0)),
                ('lpg', models.FloatField(default=0)),
                ('oil', models.FloatField(default=0)),
                ('metalBurned', models.FloatField(default=0)),
                ('glassBurned', models.FloatField(default=0)),
                ('paperBurned', models.FloatField(default=0)),
                ('organicWaste', models.FloatField(default=0)),
                ('electricityConsumed', models.FloatField(default=0)),
                ('waterConsumed', models.FloatField(default=0)),
                ('paperConsumed', models.FloatField(default=0)),
                ('cf', models.FloatField(blank=True, null=True)),
                ('time_calculated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
