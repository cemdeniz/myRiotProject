from django.contrib import admin

from .models import Summoner, Player, MatchData

admin.site.register(Summoner)
admin.site.register(Player)
admin.site.register(MatchData)
