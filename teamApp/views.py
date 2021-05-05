from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Profile, Team, UserTag, TeamTag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

loggedIn = True

class IndexView(View):

    def get(self, request):
        user = request.user
        allTeams = Team.objects.order_by("-members_needed")[:6]
        form = AuthenticationForm()
        context = {
            'allTeams': allTeams,
            'form': form,
            'user': user
        }
        if user.is_authenticated:
            context['userTeams'] = user.team_set.all().order_by("-members_needed")[:6]

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

        user = request.user
        allTeams = Team.objects.order_by("-members_needed")[:6]
        context = {
            'form': form,
            'allTeams': allTeams,
        }
        if user.is_authenticated:
            context['userTeams'] = user.team_set.all().order_by("-members_needed")[:6]

        return render(request, "teamApp/index.html", context)

class ProfileView(View):
    def get(self, request, usr):
        user = User.objects.get(username = usr)
        tags = user.usertag_set.all()
        profile = get_object_or_404(Profile, pk=user)
        teams = user.team_set.all().order_by("-members_needed")

        context = {
            'profile': profile,
            'user': user,
            'teams': teams,
            'tags': tags
        }
        if request.user.username == usr:
            context['isAuthenticated'] = True
            context['isProfileUser'] = True
        else:
            if request.user.is_authenticated:
                # if the viewer is logged in but not page owner
                context['isAuthenticated'] = True
                context['isProfileUser'] = False
            else:
                # if the viewer is not logged in
                context['isAuthenticated'] = False
                context['isProfileUser'] = False

        return render(request, 'teamApp/profile.html', context)

class EditProfileView(View):
    pass

class MyTeamsView(View):
    # return HttpResponse("hello this is where the teams are")
    pass

class TeamView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        members = User.objects.filter(team=team)
        tags = team.teamtag_set.all()
        context = {
            'team':team,
            'members': members,
            'tags':tags
        }
        if request.user in members:
            context["isMember"] = True
        else:
            context["isMember"] = False
        return render(request, 'teamApp/team.html', context)

    def post(self, request):
        pass

class EditTeamView(View):
    # return HttpResponse("hello this is the team editor for team %s" % team_id)
    pass

class CreateView(View):
    def get(self, request):
        user = request.user
        context = {'user':user}
        if user.is_authenticated:
            context["isAuthenticated"] = True
        else:
            context["isAuthenticated"] = True

        return render(request, 'teamApp/create.html', context)

    def post(self, request):
        tags = request.POST["tags"]
        tags = tags.split(', ')
        newTeam = Team(
            project_name = request.POST["teamName"],
            members_needed = request.POST["membersNeeded"],
            project_description = request.POST["teamDescription"]
        )
        newTeam.save()
        newTeam.members.add(request.user)

        for tag in tags:
            teamTag = TeamTag(name=tag, teamTagged=newTeam)
            teamTag.save()
        return redirect('index')

class RecView(View):
    pass

class RequestsView(View):
    pass
