from django.contrib import admin
from .models import Profile, Team, UserTag, TeamTag

admin.site.register(UserTag)
admin.site.register(TeamTag)
admin.site.register(Profile)
admin.site.register(Team)
