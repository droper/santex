# encoding: utf-8
"""Serializers for the models in api"""

from rest_framework import serializers

from api.models import Competition, Team, Player


class CompetitionSerializer(serializers.ModelSerializer):
    """Serializer for Competition"""

    class Meta:
        model = Competition
        exclude = ["id"]


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team"""

    class Meta:
        model = Team
        exclude = ["id"]


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for Player"""

    class Meta:
        model = Player
        exclude = ["id", "team", "type"]
