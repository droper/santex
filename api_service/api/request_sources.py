# encoding: utf-8
"""Functions that obtain data from different sources."""

import requests

import datetime


class RequestSource:
    """Class with functions for each kind of source"""

    header = {"X-Auth-Token": "22eefbd381c04a66bfcb7cb0d1324eda"}
    url = "http://api.football-data.org/v4/"
    competitions_name = "competitions"

    @classmethod
    def competition(cls, league_code):
        """
        Returns the information obtained from football-data.

        To obtain the information these steps are followed:
        * Request /competitions and obtain all the competitions (leagues) data
        * Search for the league_code in the competitions data
        * Return a dict with the competition data.
        """

        competitions_url = "".join([cls.url, cls.competitions_name])

        response = requests.get(competitions_url, headers=cls.header)
        competitions_json = response.json()

        if (
            cls.competitions_name in competitions_json
            and len(competitions_json[cls.competitions_name]) > 0
        ):
            for competition in competitions_json[cls.competitions_name]:
                print(competition)
                if competition["code"] == league_code:
                    return competition

        return {}

    @classmethod
    def competition_teams(cls, competition_id, year=datetime.date.today().year):
        """
        Returns the teams in a competition.

        * Request competitions/<id>/teams?year=<year>, using the present year
        * Create a list of dicts with the team and players data.
        * Return the list
        """

        competition_teams_url = "".join(
            [cls.url, f"{cls.competitions_name}/{competition_id}/teams"]
        )

        response = requests.get(
            competition_teams_url, {"season": year}, headers=cls.header
        )
        teams_json = response.json()

        if "teams" in teams_json:
            return teams_json["teams"]

        return []

    @classmethod
    def team(cls, code):
        """
        Returns a team data
        """

        teams_url = "".join([cls.url, "teams"])

        response = requests.get(teams_url, headers=cls.header)
        teams_json = response.json()

        if "teams" in teams_json:
            for team in teams_json["teams"]:
                if team["tla"] == code:
                    return team

        return {}
