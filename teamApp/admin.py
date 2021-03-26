from django.contrib import admin
from .models import Profile, Team, Tag

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Team)
