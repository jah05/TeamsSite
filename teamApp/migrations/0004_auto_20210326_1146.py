# Generated by Django 3.1.6 on 2021-03-26 18:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamApp', '0003_auto_20210326_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
