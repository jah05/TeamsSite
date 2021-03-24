# Generated by Django 3.1.6 on 2021-03-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamApp', '0003_auto_20210309_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='team',
            name='project_name',
            field=models.CharField(default='Untitled', max_length=64),
        ),
    ]