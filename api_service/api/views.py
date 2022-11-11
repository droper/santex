# encoding: utf-8
"""Views for the api app"""

from datetime import datetime
import requests

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Competition, Team, Player
from api.serializers import CompetitionSerializer, TeamSerializer, PlayerSerializer

from api.request_sources import RequestSource


class ImportLeagueView(APIView):
    """
    Endpoint to import and save the Competition, Team and
    Player data
    """

    serializer_class = CompetitionSerializer

    def post(self, request):
        """Save the Competition, teams and players data"""

        if "league_code" in request.data:
            print(RequestSource.competition(request.data["league_code"]))
            return Response()

        return Response()


class PlayersView(generics.ListAPIView):
    """Return the players of all teams participating in a league"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request):
        """Return all the players from the teams in a league"""

        return Response()


class TeamView(generics.ListAPIView):
    """List data and, optionally, the players from a Team"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get(self, request):
        """Return Team's data"""

        return Response()


class TeamPlayersView(generics.ListAPIView):
    """List the players of a team"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request):
        """Return the players of a team"""

        return Response()
