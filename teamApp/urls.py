from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:usr>/', views.ProfileView.as_view(), name='profile'),
    path('teams/myteams', views.MyTeamsView.as_view(), name='teams'),
    path('teams/<int:team_id>', views.TeamView.as_view(), name='team profile'),
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('create', views.CreateView.as_view(), name='create')
]
