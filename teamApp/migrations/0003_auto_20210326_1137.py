# Generated by Django 3.1.6 on 2021-03-26 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamApp', '0002_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='teamTagged',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='teamApp.team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='userTagged',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ForeignKey(blank=True, default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
