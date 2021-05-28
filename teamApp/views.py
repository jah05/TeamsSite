from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Profile, Team, UserTag, TeamTag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

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
        context["teamCreated"] = False
        return render(request, 'teamApp/create.html', context)

    def post(self, request):
        if request.POST["teamCreated"] == "False":
            tags = request.POST["tags"]
            tags = tags.split(', ')
            newTeam = Team(
                project_name = request.POST["teamName"],
                members_needed = request.POST["membersNeeded"],
                project_description = request.POST["teamDescription"]
            )
            newTeam.save()
            newTeam.members.add(request.user)
            newTeam.num_members += 1
            newTeam.save()

            for tag in tags:
                teamTag = TeamTag(name=tag, teamTagged=newTeam)
                teamTag.save()
            context = {"teamCreated": True}

            candidates = []
            for tag in tags:
                # individual instances of tag for example multiple athlete tags
                relevant_tags = UserTag.objects.filter(name=tag)
                for t in relevant_tags:
                    if (t.userTagged in candidates) == False:
                        candidates.append(t.userTagged)

            data = []
            for candidate in candidates:
                # [[c0, s0], [c1, s1],..., [cn-1, sn-1]]
                score = self.score(candidate, tags);
                try:
                    data.append([candidate, score, score/len(tags) * 100])
                except ZeroDivisionError:
                    pass

            data.sort(key=lambda x: x[1])
            context["recs"] = data
            context["numTags"] = len(tags)
            context["teamId"] = newTeam.id

            return render(request, 'teamApp/create.html', context)
        else:
            team = get_object_or_404(Team, pk=request.POST["teamId"])
            c_list = request.POST.getlist('candidates')
            for username in c_list:
                if username != request.user.username:
                    team.members.add(User.objects.get(username = username))
                    team.num_members += 1
                    team.save()
            return redirect("index")

    def score(self, candidate, teamTags):
        score = 0
        candidateTags = candidate.usertag_set.all()
        for candidateTag in candidateTags:
            if candidateTag.name in teamTags:
                score += 1

        return score

class RequestsView(View):
    pass
