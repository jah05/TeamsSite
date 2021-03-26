from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Profile, Team, Tag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

loggedIn = True

# Create your views here.
class IndexView(View):
    allTeams = Team.objects.order_by("-members_needed")

    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form':form,
            'allTeams': self.allTeams,
            'user': request.user
        }
        return render(request, 'teamApp/index.html', context)

    def post(self, request):
        pass

class ProfileView(View):
    def get(self, request, usr):
        user = User.objects.get(username = usr)
        tags = user.tag_set.all()
        profile = get_object_or_404(Profile, pk=user)
        context = {
            'username': usr,
            'profile':profile,
        }
        return render(request, 'teamApp/profile.html', context)

    def post(self, request):
        pass

class EditProfileView(View):
    pass

class MyTeamsView(View):
    # return HttpResponse("hello this is where the teams are")
    pass

class TeamView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        context = {
        }
        return render(request, 'teamApp/team.html', context)

    def post(self, request):
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
