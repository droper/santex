# encoding: utf-8
"""Tests for api_service"""

import requests

from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Competition, Team, Player
from api.request_sources import RequestSource


class RequestSourceTest(APITestCase):
    """Test RequestSource class methods"""

    @patch("requests.get")
    def test_competition(self, get_request_mock):
        """
        Test that the competition method returns the competition with the requested code
        """

        # The mocked return for the /competitions endpoint in api.football-data.org/v4
        get_return_value = {
            "count": 166,
            "filters": {},
            "competitions": [
                {
                    "id": 2006,
                    "area": {"id": 2001, "name": "Africa", "code": "AFR", "flag": None},
                    "name": "WC Qualification CAF",
                    "code": "QCAF",
                    "type": "CUP",
                    "emblem": None,
                    "plan": "TIER_FOUR",
                    "currentSeason": {
                        "id": 555,
                        "startDate": "2019-09-04",
                        "endDate": "2021-11-16",
                        "currentMatchday": 6,
                        "winner": None,
                    },
                    "numberOfAvailableSeasons": 2,
                    "lastUpdated": "2022-03-13T18:51:44Z",
                }
            ],
        }

        # If the code exists in the data, return the competition data
        get_request_mock.return_value.json.return_value = get_return_value
        self.assertEqual(
            RequestSource.competition("QCAF"), get_return_value["competitions"][0]
        )

        # If the code does not exist, return and empty dict
        self.assertEqual(RequestSource.competition("code"), {})

    @patch("requests.get")
    def test_competition_teams(self, get_request_mock):
        """
        Test that the competition_teams method returns the teams in a competition
        """

        # The mocked return for the competitions/<id>/teams endpoint in api.football-data.org/v4
        get_return_value = {
            "count": 20,
            "filters": {"season": "2022"},
            "competition": {
                "id": 2013,
                "name": "Campeonato Brasileiro Série A",
                "code": "BSA",
                "type": "LEAGUE",
                "emblem": "https://crests.football-data.org/764.svg",
            },
            "season": {
                "id": 1377,
                "startDate": "2022-04-10",
                "endDate": "2022-11-13",
                "currentMatchday": 38,
                "winner": None,
            },
            "teams": ["Team 1", "Team 2"],
        }

        # If the code exists, return the teams
        get_request_mock.return_value.json.return_value = get_return_value
        self.assertEqual(
            RequestSource.competition_teams(2013), get_return_value["teams"]
        )

        # If the competition id does not exist, return and empty list
        get_request_mock.return_value.json.return_value = {}
        self.assertEqual(RequestSource.competition_teams(1), [])

    @patch("requests.get")
    def test_team(self, get_request_mock):
        """
        Test that the team method returns the team data
        """

        get_return_value = {
            "teams": [
                {
                    "id": 1,
                    "name": "1. FC Köln",
                    "shortName": "1. FC Köln",
                    "tla": "KOE",
                },
                {
                    "id": 2,
                    "name": "TSG 1899 Hoffenheim",
                    "shortName": "Hoffenheim",
                    "tla": "TSG",
                },
            ]
        }

        # If the code exist, return and empty dict
        get_request_mock.return_value.json.return_value = get_return_value
        self.assertEqual(RequestSource.team("TSG"), get_return_value["teams"][1])

        # If code does not exist, return and empty list
        get_request_mock.return_value.json.return_value = {}
        self.assertEqual(RequestSource.team("no"), {})


class ImportLeagueTest(APITestCase):
    """Test for /import_league endpoint"""

    @patch("api.request_sources.RequestSource.competition_teams")
    @patch("api.request_sources.RequestSource.competition")
    def test_import(self, competition_get_mock, teams_get_mock):
        """
        Test that the /import_league saves the Competition, Team
        and Player data
        """

        url = reverse("import_league")

        # The data to be mocked from RequestSource.competition
        competition_input_data = {
            "id": 1,
            "name": "league name",
            "code": "code",
            "area": {"name": "area"},
        }

        # The data to be mocked from RequestSource.competition_teams
        teams_input_data = [
            {
                "name": "Team name",
                "shortName": "Team",
                "tla": "tla",
                "area": {"name": "area"},
                "address": "address 1",
                "coach": {
                    "name": "coach name",
                    "dateOfBirth": "1980-06-10",
                    "nationality": "Argentina",
                },
                "squad": [
                    {
                        "name": "player name 1",
                        "position": "position 1",
                        "dateOfBirth": "2001-07-16",
                        "nationality": "Peru",
                    },
                    {
                        "name": "player name 2",
                        "position": "position 2",
                        "dateOfBirth": "2000-08-01",
                        "nationality": "Bolivia",
                    },
                ],
            }
        ]

        # The output data from the endPoint /import_league
        competition_output_data = {
            "name": "league name",
            "code": "code",
            "area_name": "area",
        }

        team_data = {
            "name": "Team name",
            "short_name": "Team",
            "tla": "tla",
            "area_name": "area",
            "address": "address 1",
            "competition": [1],
        }
        player1_data = {
            "name": "player name 1",
            "position": "position 1",
            "date_of_birth": "2001-07-16",
            "nationality": "Peru",
        }
        player2_data = {
            "name": "player name 2",
            "position": "position 2",
            "date_of_birth": "2000-08-01",
            "nationality": "Bolivia",
        }

        return_data = {
            "competition": competition_output_data,
            "teams": [team_data],
            "players": [player1_data, player2_data],
        }

        # Mock returns
        competition_get_mock.return_value = competition_input_data
        teams_get_mock.return_value = teams_input_data

        # Call the endpoint with league_code and verify that it returns the required data
        # and saves the data
        response = self.client.post(
            url, {"league_code": competition_input_data["code"]}, format="json"
        )
        self.assertEqual(response.json(), return_data)

        # If called with no post parameter, the endpoint returns an empty dict
        response = self.client.post(url, format="json")
        self.assertEqual(response.json(), {})

        # If called with a non-existent league_code, the endpoint returns an empty dict
        competition_get_mock.return_value = {}
        response = self.client.post(url, {"league_code": "no code"}, format="json")
        self.assertEqual(response.json(), {})

        # If called with no squad the endpoint must return the coach data
        del teams_input_data[0]["squad"]
        response = self.client.post(url, {"league_code": "no code"}, format="json")
        self.assertEqual(response.json(), {})


class GetEndpointTest(APITestCase):
    """Base class for testing the get endpoints"""

    @classmethod
    def setUpTestData(cls):
        """Create objects for the database"""

        # Create objects in the database
        cls.competition = Competition(
            id=1, name="name 1", code="code", area_name="area 1"
        )
        cls.competition.save()

        cls.team1 = Team(
            id=1,
            name="name 1",
            tla="code1",
            short_name="sn1",
            area_name="area 1",
            address="address 1",
        )
        cls.team1.save()
        cls.team1.competition.add(cls.competition)
        cls.team1.save()
        cls.team2 = Team(
            id=2,
            name="name 2",
            tla="code2",
            short_name="sn2",
            area_name="area 2",
            address="address 2",
        )
        cls.team2.save()
        cls.team2.competition.add(cls.competition)
        cls.team2.save()

        cls.player1 = Player(
            id=1,
            name="player 1",
            position="position 1",
            date_of_birth="1999-10-06",
            nationality="Peru",
            team=cls.team1,
            type="PL",
        )
        cls.player1.save()
        cls.player2 = Player(
            id=2,
            name="player 2",
            position="position 2",
            date_of_birth="1998-05-16",
            nationality="Bolivia",
            team=cls.team2,
            type="PL",
        )
        cls.player2.save()

        cls.team1_response_data = {
            "name": "name 1",
            "tla": "code1",
            "short_name": "sn1",
            "area_name": "area 1",
            "address": "address 1",
            "competition": [1],
        }

        cls.team2_response_data = {
            "name": "name 2",
            "tla": "code2",
            "short_name": "sn2",
            "area_name": "area 2",
            "address": "address 2",
            "competition": [2],
        }

        cls.player1_response_data = {
            "name": "player 1",
            "position": "position 1",
            "date_of_birth": "1999-10-06",
            "nationality": "Peru",
        }

        cls.player2_response_data = {
            "name": "player 2",
            "position": "position 2",
            "date_of_birth": "1998-05-16",
            "nationality": "Bolivia",
        }


class PlayersTest(GetEndpointTest):
    """Test for /players endpoint"""

    def test_players(self):
        """
        Test that the players endpoint return all the players in the
        teams participating in a League.
        """

        url = reverse("players")

        # The data that must be in the response
        response_data = [self.player1_response_data, self.player2_response_data]

        # Request the endpoint with the competition code to retrieve all the players
        response = self.client.get(url, {"league_code": "code"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), response_data)

        # If requested with no parameter or with an unexistant one the response
        # is an error message
        response = self.client.get(url, {"league_code": "no code"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no league with code no code")

        # If requested with no parameter or with an unexistant one the response
        # is an error message
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no league with code None")


class TeamTest(GetEndpointTest):
    """Test for /team endpoint"""

    def test_team(self):
        """
        Test that the /team endpoint returns the team data and the players data.
        """

        url = reverse("team")

        # If requested with an existent competition code, the response
        # is the team data
        response = self.client.get(url, {"tla": "code1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"team": self.team1_response_data})

        # If requested an unexistant one the response is an error message
        response = self.client.get(url, {"tla": "no code"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no team with tla no code")

        # If requested with an existent competition code, the response
        # is the team data
        response = self.client.get(url, {"tla": "code1", "players": "T"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"team": self.team1_response_data, "players": [self.player1_response_data]},
        )

        # If requested with no parameter the response is an empty dict
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no team with tla None")


class TeamPlayersTest(GetEndpointTest):
    """Test for /team/players endpoint"""

    def test_team_players(self):
        """
        Test that the endpoint /team/players returns the players of the team
        """

        url = reverse("team_players")

        # Test the endpoint with a team code
        response = self.client.get(url, {"team_code": "code1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [self.player1_response_data])

        # Test the endpoint with an invalid team code
        response = self.client.get(url, {"team_code": "no code"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no team with code no code")

        # If requested with no parameter the response is an empty dict
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "There is no team with code None")
