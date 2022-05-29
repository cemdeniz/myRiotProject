from django.contrib import admin

from .models import Question, Choice, Player, Summoner

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Player)
admin.site.register(Summoner)
