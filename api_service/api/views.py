# encoding: utf-8
"""Views for the api app"""

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.forms.models import model_to_dict

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
            if not Competition.objects.filter(
                code=request.data["league_code"]
            ).exists():
                competition_data = RequestSource.competition(
                    request.data["league_code"]
                )

                # If there is no data in competition, return empty value
                if not competition_data:
                    return Response(return_data)

                data = {
                    "name": competition_data["name"],
                    "code": competition_data["code"],
                    "area_name": competition_data["area"]["name"],
                }

                serializer = self.serializer_class(data=data)
                if not serializer.is_valid(raise_exception=True):
                    return Response(serializer.data, status=201)
                competition = serializer.save()
                return_data["competition"] = data

                # Obtain the competition teams and save them if the team is not already saved
                competition_team_data = RequestSource.competition_teams(
                    competition_data["id"]
                )
                return_data["teams"] = []
                return_data["players"] = []
                for team_data in competition_team_data:
                    if Team.objects.filter(tla=team_data["tla"]).exists():
                        team = Team.objects.get(tla=team_data["tla"])
                        team.competition.add(competition)
                    else:
                        data = {
                            "name": team_data["name"],
                            "short_name": team_data["shortName"],
                            "tla": team_data["tla"],
                            "area_name": team_data["area"]["name"],
                            "address": team_data["address"][:100],
                            "competition": [competition.id],
                        }
                        serializer = TeamSerializer(data=data)
                        if not serializer.is_valid(raise_exception=True):
                            return Response(serializer.data, status=201)
                        team = serializer.save()

                        return_data["teams"].append(data)

                        # If there is a squad save the players, if not, save the coach.
                        if "squad" in team_data:
                            for player_data in team_data["squad"]:
                                if not Player.objects.filter(
                                    name=player_data["name"]
                                ).exists():
                                    data = {
                                        "name": player_data["name"],
                                        "position": player_data["position"],
                                        "date_of_birth": player_data["dateOfBirth"],
                                        "nationality": player_data["nationality"],
                                    }
                                    serializer = PlayerSerializer(data=data)
                                    if not serializer.is_valid(raise_exception=True):
                                        return Response(serializer.data, status=201)
                                    player = serializer.save()
                                    # Need to update the object with the team
                                    # because the serializer excludes the team
                                    player.team = team
                                    player.save()

                                    return_data["players"].append(
                                        serializer.validated_data
                                    )
                        else:
                            if not Player.objects.filter(
                                name=team_data["coach"]["name"]
                            ).exists():
                                data = {
                                    "name": team_data["coach"]["name"],
                                    "date_of_birth": team_data["coach"]["dateOfBirth"],
                                    "nationality": team_data["coach"]["nationality"],
                                    "team": team.id,
                                    "type": "CO",
                                }
                                serializer = PlayerSerializer(data=data)
                                if not serializer.is_valid(raise_exception=True):
                                    return Response(serializer.data, status=201)
                                player = serializer.save()
                                # Need to update the object with the team
                                # because the serializer excludes the team
                                player.team = team
                                player.save()

                                return_data["players"].append(serializer.validated_data)
            else:
                return Response("Competition already in the database")
        return Response(return_data)


class PlayersView(generics.ListAPIView):
    """Return the players of all teams participating in a league"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request):
        """Return all the players from the teams in a league"""

        # If there is a league_code parameter and the competition exists
        # obtain the competition, the teams associated with the competition,
        # the players of each team and return them in a list of dicts
        if (
            "league_code" in request.query_params
            and Competition.objects.filter(
                code=request.query_params.get("league_code")
            ).exists()
        ):
            competition = Competition.objects.get(
                code=request.query_params.get("league_code")
            )

            teams = Team.objects.all()
            if "team" in request.query_params and Team.objects.filter(
                tla=request.query_params.get("league_code")
            ):
                teams = teams.filter(competition=competition)

            players = []
            for team in teams:
                team_players = self.queryset.filter(team=team).values(
                    "name", "position", "date_of_birth", "nationality"
                )
                players.extend(team_players)
            return Response(players)

        return Response(
            f"There is no league with code {request.query_params.get('league_code')}"
        )


class TeamView(generics.ListAPIView):
    """List data and, optionally, the players from a Team"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get(self, request):
        """Return Team's data"""

        result = {}
        # If the tla is in the query parameters and the team exist, retrieve the team data for the response
        if "tla" in request.query_params and Team.objects.filter(
            tla=request.query_params.get("tla")
        ):
            team = Team.objects.get(tla=request.query_params.get("tla"))
            team_serializer = self.serializer_class(team)
            result["team"] = team_serializer.data

            # If the players flag is True, then retrieve the players data
            if (
                "players" in request.query_params
                and request.query_params.get("players").upper() == "T"
            ):
                players = Player.objects.filter(team=team).values()
                player_serializer = PlayerSerializer(players, many=True)
                result["players"] = player_serializer.data

            return Response(result)

        return Response(f"There is no team with tla {request.query_params.get('tla')}")


class TeamPlayersView(generics.ListAPIView):
    """List the players of a team"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get(self, request):
        """Return the players of a team"""

        # If there is a team_code parameter and the team exists return the players from the team.
        if "team_code" in request.query_params and Team.objects.filter(
            tla=request.query_params.get("team_code")
        ):
            team = Team.objects.get(tla=request.query_params.get("team_code"))
            players = Player.objects.filter(team=team).values()
            player_serializer = PlayerSerializer(players, many=True)
            return Response(player_serializer.data)

        return Response(
            f"There is no team with code {request.query_params.get('team_code')}"
        )
