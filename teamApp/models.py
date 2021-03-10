from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.CharField(max_length=10)
    tags = models.ManyToManyField(Tag)
    # profile_picture = models.ImageField()
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default="Unnamed")
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Team(models.Model):
    project_id = models.CharField(max_length=10)
    project_name = models.CharField(max_length=10, default="Untitled")
    num_members = models.IntegerField(default=0)
    members_needed = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    project_description = models.TextField(max_length=1000)
    members = models.ManyToManyField(Profile)
    # logo = models.ImageField()

    def __str__(self):
        return self.project_name
