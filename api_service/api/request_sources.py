# encoding: utf-8
"""Functions that obtain data from different sources."""

import requests


class RequestSource:
    """Class with functions for each kind of source"""

    header = {"X-Auth-Token": "22eefbd381c04a66bfcb7cb0d1324eda"}
    url = "http://api.football-data.org/v4/"

    @classmethod
    def competition(cls, league_code):
        """
        Returns the information obtained from football-data.

        To obtain the information this steps are followed:
        * Request /competitions and obtain all the competitions (leagues) data
        * Search for the league_code in the competitions data
        * Return a dict with the competition data.
        """

        competitions_url = ''.join([cls.url, "competitions"])

        response = requests.get(competitions_url, headers=cls.header)
        competitions_json = response.json()

        for competition in competitions_json["competitions"]:
            if competitions["code"] == league_code:
                return competition

        return competitions_json


    def competition_teams(self, competition_id):
        """
        Search for the teams in a competition.

        * Request competitions/<id>/teams?year=<year>, using the present year
        * Create a list of dicts with the team and players data.
        * Return the list
        """

        competition_teams_url = ''.join([self.url, f"competitions/{competition_id}/teams"])

        response = requests.get(competition_teams_url, headers=self.header)
