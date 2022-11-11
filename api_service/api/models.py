# encoding: utf-8
"""Models for api app"""

from django.db import models


class Competition(models.Model):
    """Model to store the competitions"""

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    area_name = models.CharField(max_length=100)
    area_id = models.IntegerField()

    class Meta:
        ordering = ['name']


class Team(models.Model):
    """Model to store the teams"""

    name = models.CharField(max_length=100)
    tla = models.CharField(max_length=10)
    short_name = models.CharField(max_length=10)
    area_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    competition = models.ManyToManyField(Competition)

    class Meta:
        ordering = ['name']


class Player(models.Model):
    """Model to store the players"""

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=30)
    date_of_birth = models.DateField(max_length=10)
    nationality = models.CharField(max_length=30)
    team = models.ForeignKey(Team, models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']