from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Profile, Team, UserTag, TeamTag
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

class IndexView(View):
    """
    This view is responsible for the index page
    """
    def get(self, request):
        user = request.user
        # get teams that need members most from all teams
        allTeams = Team.objects.order_by("-members_needed")[:8]

        context = {
            'allTeams': allTeams,
            'user': user
        }
        if user.is_authenticated:
            # these are teams that the user is part of
            context['userTeams'] = user.team_set.all().order_by("-members_needed")[:8]

        return render(request, 'teamApp/index.html', context)

    def post(self, request):
        # check for login or logout request
        if 'login' in request.POST.keys():
            return redirect("login")

        if 'logout' in request.POST.keys():
            logout(request)

        user = request.user
        # rebuild context for display again
        allTeams = Team.objects.order_by("-members_needed")[:10]
        context = {
            'allTeams': allTeams,
        }
        if user.is_authenticated:
            context['userTeams'] = user.team_set.all().order_by("-members_needed")[:8]

        return render(request, "teamApp/index.html", context)

class LoginView(View):
    """This view is responsible for the login page"""
    def get(self, request):
        # only allow login page if user isn't logged in
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            # success is used as a flag to see if log in was good
            context = {'form':form, 'success':True}
            return render(request, 'teamApp/login.html', context)
        else:
            return redirect('index')

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user = user)
                return redirect("index")
        else:
            # if log in fails notify the page of failure and rebuild page
            form = AuthenticationForm()
            context = {'form':form, 'success':False}
            return render(request, 'teamApp/login.html', context)

class ProfileView(View):
    """This view is responsible for the profile page"""
    def get(self, request, usr):
        user = User.objects.get(username = usr)
        tags = user.usertag_set.all()
        profile = get_object_or_404(Profile, pk=user)
        teams = user.team_set.all().order_by("-members_needed")

        context = {
            'profile': profile,
            'page_user':usr,
            'viewer': request.user,
            'teams': teams,
            'tags': tags,
            'edit': False,
        }
        context['isAuthenticated'] = request.user.is_authenticated
        context['isProfileUser'] = request.user.username==usr
        return render(request, 'teamApp/profile.html', context)

    def post(self, request, usr):
        user = User.objects.get(username = usr)
        profile = get_object_or_404(Profile, pk=user)

        # if the edit is submitted
        if 'editsubmit' in request.POST.keys():
            profile.name = request.POST["nInput"]
            profile.age = request.POST["aInput"]
            profile.city = request.POST["cInput"]
            profile.bio = request.POST["bInput"]
            tags = request.POST["tags"]
            tags = tags.split(', ')

            # delete old tags
            ogTags = user.usertag_set.all()
            for tag in ogTags:
                tag.delete()

            for tag in tags:
                userTag = UserTag(name=tag, userTagged=user)
                userTag.save()

            profile.save()
            return self.get(request, usr)
        # otherwise check for edit button or display normally
        else:
            tags = user.usertag_set.all()
            teams = user.team_set.all().order_by("-members_needed")

            context = {
                'profile': profile,
                'user': user,
                'teams': teams,
                'tags': tags,
                'edit': 'edit' in request.POST.keys(),
            }
            context['isAuthenticated'] = request.user.is_authenticated
            context['isProfileUser'] = request.user.username==usr
            temp = []
            for tag in tags:
                temp.append(tag.name)
            context['tagStr'] = ', '.join(temp)
            return render(request, 'teamApp/profile.html', context)

class MyTeamsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            context={'allTeams':request.user.team_set.all().order_by("-members_needed"),
            'user':request.user}
        return render(request, 'teamApp/myteams.html', context)

class TeamView(View):
    """This view is responsible for the profile page"""
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        members = User.objects.filter(team=team)
        # get tags of the team
        tags = team.teamtag_set.all()
        context = {
            'team':team,
            'members': members,
            'tags':tags,
            'edit':False
        }
        # check if user is part of the team
        context["isMember"] = request.user in members
        return render(request, 'teamApp/team.html', context)

    def post(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        members = User.objects.filter(team=team)
        tags = team.teamtag_set.all()
        if 'editsubmit' in request.POST.keys():
            if 'dropdown' in request.POST.keys():
                team.num_members += 1
                team.members.add(User.objects.get(username=request.POST["dropdown"]))
            team.project_name = request.POST["nInput"]
            team.members_needed = request.POST["mInput"]
            team.project_description = request.POST["dInput"]

            tags = request.POST["tags"]
            tags = tags.split(', ')

            # delete old tags
            ogTags = team.teamtag_set.all()
            for tag in ogTags:
                tag.delete()

            for tag in tags:
                teamTag = TeamTag(name=tag, teamTagged=team)
                teamTag.save()
            team.save()
            return self.get(request, team_id)
        elif 'delete' in request.POST.keys():
            team.delete()
            return redirect('index')
        else:
            context = {
                'team':team,
                'members': members,
                'tags':tags,
                'edit': 'edit' in request.POST.keys()
            }

            candidates = User.objects.all().difference(members)
            context["candidates"] = candidates
            # check if user is part of the team
            context["isMember"] = request.user in members
            temp = []
            for tag in tags:
                temp.append(tag.name)
            context['tagStr'] = ', '.join(temp)
            return render(request, 'teamApp/team.html', context)

class CreateView(View):
    """This view is responsible for the create page"""
    def get(self, request):
        user = request.user
        context = {'user':user}
        # only enable create page once user is logged in
        if user.is_authenticated:
            context["isAuthenticated"] = True
        else:
            return redirect("index")
        # flag to tell post function whether to display the creation form or candidates
        context["teamCreated"] = False
        return render(request, 'teamApp/create.html', context)

    def post(self, request):
        # if the user has entered data
        if request.POST["teamCreated"] == "False":
            tags = request.POST["tags"]
            tags = tags.split(', ') # split tags up
            newTeam = Team(
                project_name = request.POST["teamName"],
                members_needed = request.POST["membersNeeded"],
                project_description = request.POST["teamDescription"]
            )
            newTeam.save()

            # change team attributes
            newTeam.members.add(request.user)
            newTeam.num_members += 1
            newTeam.save()

            # save inputted tags
            for tag in tags:
                teamTag = TeamTag(name=tag, teamTagged=newTeam)
                teamTag.save()
            context = {"teamCreated": True}

            candidates = []
            for tag in tags:
                # individual instances of tag, for example multiple athlete tags
                relevant_tags = UserTag.objects.filter(name=tag)
                for t in relevant_tags:
                    # make sure no duplicate candidates
                    if (t.userTagged in candidates) == False:
                        candidates.append(t.userTagged)

            data = []
            for candidate in candidates:
                # [[c0, s0], [c1, s1],..., [cn-1, sn-1]] c-candidate s-score
                score = self.score(candidate, tags);
                # make sure it doesn't crash if no tags are added
                try:
                    data.append([candidate, score, score/len(tags) * 100])
                except ZeroDivisionError:
                    pass

            data.sort(key=lambda x: x[1], reverse=True) # sort by score for usability
            context["recs"] = data
            context["numTags"] = len(tags)
            context["teamId"] = newTeam.id

            return render(request, 'teamApp/create.html', context)
        else:
            # team is created and candidates are selected
            team = get_object_or_404(Team, pk=request.POST["teamId"])
            c_list = request.POST.getlist('candidates')
            for username in c_list:
                # make sure creator isn't included twice
                if username != request.user.username:
                    team.members.add(User.objects.get(username = username))
                    team.num_members += 1
                    team.save()
            return redirect("team profile", team.id)

    def score(self, candidate, teamTags):
        score = 0
        candidateTags = candidate.usertag_set.all()
        for candidateTag in candidateTags:
            if candidateTag.name in teamTags:
                score += 1

        return score

class RegisterView(View):
    """This view is responsible for the register page"""
    def get(self, request):
        return render(request, "teamApp/register.html", {'error':''})

    def post(self, request):
        if request.POST["password"] == request.POST["cpassword"]:   # check if passwords match
            # look for blank fields
            if request.POST["username"]=='' or request.POST["email"]=='' or request.POST["password"]=='' or request.POST["name"]=='' or request.POST["age"]=='' or request.POST["city"]=='':
                return render(request, "teamApp/register.html", {'error':"ERROR: fields not filled"})
            try:
                # look for existing users
                user = User.objects.get(username=request.POST["username"])
                return render(request, "teamApp/register.html", {'error':"ERROR: username taken"})
            except:
                user=User.objects.create(username=request.POST["username"], password=make_password(request.POST["password"]), email=request.POST["email"])
                user.save()
                login(request, user)

                profile = Profile(user=user, city=request.POST["city"], name=request.POST["name"], age=int(request.POST["age"]), bio=request.POST["bio"])
                profile.save()

                tags = request.POST["tags"].split(', ')
                for tag in tags:
                    userTag = UserTag(name=tag, userTagged=user)
                    userTag.save()

                return redirect("index")
        else:
            return render(request, "teamApp/register.html", {'error':"ERROR: passwords do not match"})
