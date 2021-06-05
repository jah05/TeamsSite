from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default="Unnamed")
    bio = models.TextField(max_length=1024, default='')
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Team(models.Model):
    project_name = models.CharField(max_length=200, default="Untitled")
    num_members = models.IntegerField(default=0)
    members_needed = models.IntegerField(default=0)
    project_description = models.TextField(max_length=1000)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.project_name

class UserTag(models.Model):
    name = models.CharField(max_length=100)
    userTagged = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TeamTag(models.Model):
    name = models.CharField(max_length=100)
    teamTagged = models.ForeignKey(Team, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
