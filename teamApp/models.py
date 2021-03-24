from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserTag(models.Model): # team tag + profile tag
    name = models.CharField(max_length=100)
    userTagged = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # profile_picture = models.ImageField()
    city = models.CharField(max_length=64)
    # name = models.CharField(max_length=64, default="Unnamed")
    bio = models.TextField(max_length=1024, default='')
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Team(models.Model):
    project_name = models.CharField(max_length=64, default="Untitled")
    num_members = models.IntegerField(default=0)
    members_needed = models.IntegerField(default=0)
    project_description = models.TextField(max_length=1000)
    members = models.ManyToManyField(Profile)
    # add photo

    def __str__(self):
        return self.project_name



class TeamTag(models.Model):
    name = models.CharField(max_length=100)
    teamTagged = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return self.name
