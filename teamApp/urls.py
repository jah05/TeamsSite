from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:usr>/', views.ProfileView.as_view(), name='profile'),
    path('<str:usr>/edit', views.EditProfileView.as_view(), name='edit profile'),
    path('teams/', views.MyTeamsView.as_view(), name='teams'),
    path('teams/<int:team_id>', views.TeamView.as_view(), name='team profile'),
    path('teams/<int:team_id>/edit', views.EditTeamView.as_view(), name='edit team profile'),
    path('create', views.CreateView.as_view(), name='create'),
    path('create/recs', views.RecView.as_view(), name="recommendations"),
    path('requests', views.RequestsView.as_view(), name="requests")
]
