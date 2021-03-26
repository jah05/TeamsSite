# Generated by Django 3.1.6 on 2021-03-25 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('city', models.CharField(max_length=64)),
                ('bio', models.TextField(default='', max_length=1024)),
                ('age', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='Untitled', max_length=64)),
                ('num_members', models.IntegerField(default=0)),
                ('members_needed', models.IntegerField(default=0)),
                ('project_description', models.TextField(max_length=1000)),
                ('members', models.ManyToManyField(to='teamApp.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('teamTagged', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teamApp.team')),
                ('userTagged', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
