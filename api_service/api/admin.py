# encoding: utf-8
"""Admin configurations for api"""

from django.contrib import admin

from .models import Competition, Team, Player


admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Player)
