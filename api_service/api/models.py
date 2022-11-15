# encoding: utf-8
"""Models for api app"""

from django.db import models


class Competition(models.Model):
    """Model to store the competitions"""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    area_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return " ".join([self.name, self.code])


class Team(models.Model):
    """Model to store the teams"""

    name = models.CharField(max_length=100)
    tla = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=30)
    area_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    competition = models.ManyToManyField(Competition)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return " ".join([self.name, self.tla])


class Player(models.Model):
    """Model to store the players"""

    PLAYER = "PL"
    COACH = "CO"

    TYPE_TEAM_MEMBER = [(PLAYER, "Player"), (COACH, "Coach")]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=30, blank=True, null=True)
    team = models.ForeignKey(Team, models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=2, choices=TYPE_TEAM_MEMBER, default=PLAYER)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return " ".join([self.name, self.type])
