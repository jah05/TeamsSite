from django.contrib import admin
from .models import UserTag, Profile, Team, TeamTag

admin.site.register(UserTag)
admin.site.register(TeamTag)
admin.site.register(Profile)
admin.site.register(Team)
