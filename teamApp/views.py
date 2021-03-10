from django.shortcuts import render
from django.http import HttpResponse

loggedIn = True

# Create your views here.
def index(request):
    return HttpResponse("hello this is index")

def profile(request, profile_id):
    return HttpResponse("hello this is profile page of user %s" % profile_id)

def edit_profile(request, profile_id):
    return HttpResponse("hello this is edit profile page for user %s" % profile_id)

def teams(request):
    return HttpResponse("hello this is where the teams are")

def team_profile(request, team_id):
    return HttpResponse("hello this is the team profile for team %s" %team_id)

def edit_team(request, team_id):
    return HttpResponse("hello this is the team editor for team %s" %team_id)

def create(request):
    return HttpResponse("hello, create your team here")

def recs(request):
    return HttpResponse("here choose your members")

def requests(request):
    return HttpResponse("here you look at your team requests")
