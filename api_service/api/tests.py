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

    def test_import(self):
        """
        Test that the /import_league saves the Competition, Team
        and Player data
        """

        url = reverse("players")


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
