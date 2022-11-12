# encoding: utf-8
"""Views for the api app"""

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

        return_data = {}

        if "league_code" in request.data:
            # Obtain competition and save in the database
            if not Competition.objects.filter(code=request.data["league_code"]).exists():
                competition_data = RequestSource.competition(request.data["league_code"])

                # If there is no data in competition, return empty value
                if not competition_data:
                    return Response()

                data = {
                    "name": competition_data["name"],
                    "code": competition_data["code"],
                    "area_name": competition_data["area"]["name"]
                }
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                competition = serializer.save()

                return_data["competition"] = data

                # Obtain the competition teams and save them if the team is not already saved
                competition_team_data = RequestSource.competition_teams(competition_data["code"])
                return_data["teams"] = []
                return_data["players"] = []
                for team_data in competition_team_data:
                    if not Team.objects.filter(tla=team_data["tla"]).exists():
                        data = {
                            "name": team_data["name"],
                            "short_name": team_data["shortName"],
                            "tla": team_data["tla"],
                            "area_name": team_data["area"]["name"],
                            "address": team_data["address"],
                            "competition": [competition.id]
                        }
                        serializer = TeamSerializer(data=data)
                        serializer.is_valid(raise_exception=True)
                        team = serializer.save()

                        return_data["teams"].append(data)

                        # Save the players
                        if "squad" in team_data:
                            for player_data in team_data["squad"]:
                                if not Player.objects.filter(name=player_data["name"]).exists():
                                    data = {
                                        "name": player_data["name"],
                                        "position": player_data["position"],
                                        "date_of_birth": player_data["dateOfBirth"],
                                        "nationality": player_data["nationality"],
                                        "team": team.id
                                    }
                                    serializer = PlayerSerializer(data=data)
                                    serializer.is_valid(raise_exception=True)
                                    serializer.save()

                                    return_data["players"].append(data)
                        else:
                            if not Player.objects.filter(name=team_data["coach"]["name"]).exists():
                                data = {
                                    "name": team_data["coach"]["name"],
                                    "date_of_birth": team_data["coach"]["dateOfBirth"],
                                    "nationality": team_data["coach"]["nationality"],
                                    "team": team.id,
                                    "type": "CO"
                                }
                                serializer = PlayerSerializer(data=data)
                                serializer.is_valid(raise_exception=True)
                                serializer.save()

                                return_data["players"].append(data)

        return Response(return_data)


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

        if "code" in request.query_params:
            return Response(RequestSource.team(request.query_params["code"]))

        return Response()


class TeamPlayersView(generics.ListAPIView):
    """List the players of a team"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request):
        """Return the players of a team"""

        return Response()
