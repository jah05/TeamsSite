from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Profile, Team, Tag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

loggedIn = True

class IndexView(View):
    allTeams = Team.objects.order_by("-members_needed")

    def get(self, request):
        user = request.user
        form = AuthenticationForm()
        context = {
            'allTeams': self.allTeams,
            'form': form,
            'user': user
        }

        return render(request, 'teamApp/index.html', context)

    def post(self, request):
        if 'logout' in request.POST.keys():
            logout(request)
            form = AuthenticationForm()
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user = user)

        context = {
            'form': form,
            'allTeams': self.allTeams,
        }

        return render(request, "teamApp/index.html", context)

class ProfileView(View):
    def get(self, request, usr):
        user = User.objects.get(username = usr)
        tags = user.tag_set.all()
        if request.user.username == usr:
            # if the user is the profile owner
            pass
        else:
            if request.user.is_authenticated:
                # if the viewer is logged in but not page owner
                pass
            else:
                # if the viewer is not logged in
                pass
        # profile = get_object_or_404(Profile, pk=user)
        # context = {
        #     'username': usr,
        #     'profile': profile,
        # }
        return render(request, 'teamApp/profile.html', context)

class EditProfileView(View):
    pass

class MyTeamsView(View):
    # return HttpResponse("hello this is where the teams are")
    pass

class TeamView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        members = team.user_set.all()
        if request.user in members:
            pass
        else:
            pass
        context = {
            'team':team
        }
        return render(request, 'teamApp/team.html', context)

    def post(self, request):
        pass

class EditTeamView(View):
    # return HttpResponse("hello this is the team editor for team %s" % team_id)
    pass

class CreateView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            pass
        else:
            pass

    def post(self, request):
        pass

class RecView(View):
    pass

class RequestsView(View):
    pass
