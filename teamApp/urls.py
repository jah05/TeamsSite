from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:profile_id>/', views.profile, name='profile'),
    path('<str:profile_id>/edit', views.edit_profile, name='edit profile'),
    path('teams/', views.teams, name='teams'),
    path('teams/<str:team_id>', views.team_profile, name='team profile'),
    path('teams/<str:team_id>/edit', views.edit_team, name='edit team profile'),
    path('create', views.create, name='create'),
    path('create/recs', views.recs, name="recommendations"),
    path('requests', views.requests, name="requests")
]
