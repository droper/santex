# encoding: utf-8

from django.contrib import admin
from django.urls import path

from api import views as api_views

urlpatterns = [
    path("import_league", api_views.ImportLeagueView.as_view(), name="import_league"),
    path("players", api_views.PlayersView.as_view(), name="players"),
    path("team", api_views.TeamView.as_view(), name="team"),
    path("team/players", api_views.TeamPlayersView.as_view(), name="team_players"),
    path("admin/", admin.site.urls),
]
