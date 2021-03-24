from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import UserTag, Profile, Team, TeamTag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

loggedIn = True

# Create your views here.
class IndexView(View):
    allTeams = Team.objects.order_by("-members_needed")[:6]

    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form':form,
            'allTeams': self.allTeams,
            'user': request.user,
        }
        return render(request, 'teamApp/index.html', context)

    def post(self, request):
        pass

class ProfileView(View):
    def get(self, request, usr):
        user = User.objects.get(username = usr)
        tags = user.userTag_set.all()
        profile = get_object_or_404(Profile, pk=user)
        context = {
            'age': profile.age,
            'username': usr,
            'tags': tags,
            'bio': profile.bio,
            'city': profile.city
        }
        return render(request, 'teamApp/profile.html')

    def post(self, request):
        pass

class EditProfileView(View):
    def get(self, request, usr):
        pass
    def post(self, request):
        pass

class MyTeamsView(View):
    # return HttpResponse("hello this is where the teams are")
    pass

class TeamView(View):
    # return HttpResponse("hello this is the team profile for team %s" % team_id)
    pass

class EditTeamView(View):
    # return HttpResponse("hello this is the team editor for team %s" % team_id)
    pass

class CreateView(View):
    # return HttpResponse("hello, create your team here")
    pass

class RecView(View):
    pass

class RequestsView(View):
    pass
