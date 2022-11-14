# encoding: utf-8
"""Tests for api_service"""

from datetime import datetime
from unittest.mock import patch

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Competition, Team, Player


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
            "name": "league name",
            "code": "code",
            "area": {"name": "area"}
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
                ]
            }
        ]

        # The output data from the endPoint /import_league
        competition_output_data = {
            "name": "league name",
            "code": "code",
            "area_name": "area"
        }

        team_data = {
            "name": "Team name",
            "short_name": "Team",
            "tla": "tla",
            "area_name": "area",
            "address": "address 1",
            "competition": [1]
        }
        player1_data = {
            "name": "player name 1",
            "position": "position 1",
            "date_of_birth": "2001-07-16",
            "nationality": "Peru",
            "team": 1
        }
        player2_data = {
            "name": "player name 2",
            "position": "position 2",
            "date_of_birth": "2000-08-01",
            "nationality": "Bolivia",
            "team": 1
        }

        return_data = {
            "competition": competition_output_data,
            "teams": [team_data],
            "players": [player1_data, player2_data]
        }

        # Mock returns
        competition_get_mock.return_value = competition_input_data
        teams_get_mock.return_value = teams_input_data

        # Call the endpoint with league_code and verify that it returns the required data
        # and saves the data
        response = self.client.post(url, {"league_code": competition_input_data["code"]}, format="json")
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


class PlayersTest(APITestCase):
    """Test for /players endpoint"""

    def test_players(self):
        """
        Test that the players endpoint return all the players in the
        teams participating in a League.
        """

        url = reverse("players")


class TeamTest(APITestCase):
    """Test for /team endpoint"""

    def test_stats(self):
        """
        Ensure we obtain the desired stats from the endpoint and
        that only a super_user can see them.
        """

        url = reverse("team")


class TeamPlayersTest(APITestCase):
    """Test for /team/players endpoint"""

    @patch("requests.get")
    def test_stock(self, request_get_mock):
        """
        Ensure we obtain the stock data and only an authenticated user
        can access
        """

        url = reverse("team_players")
