from django.contrib.auth.models import User
from django.db import models
from django.forms import TextInput, ModelForm
from django.utils import timezone
import datetime


class MatchData(models.Model):
    matchId = models.CharField(max_length=50, null=True, unique=True)
    gameDuration = models.CharField(max_length=50, null=True)
    queueId = models.CharField(max_length=50, null=True)
    mapName = models.CharField(max_length=50, null=True)
    mapDesc = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.matchId


class Summoner(models.Model):
    sname = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=50, null=True)
    tier = models.CharField(max_length=50, null=True)
    rank = models.CharField(max_length=50, null=True)
    lp = models.CharField(max_length=50, null=True)
    win = models.CharField(max_length=50, null=True)
    lose = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.sname


class Player(models.Model):
    Name = models.CharField(max_length=50, null=True)
    Champ = models.CharField(max_length=50, null=True)
    KDA = models.CharField(max_length=10, null=True)
    TotalGold = models.IntegerField(blank=True, null=True)
    SoloKill = models.IntegerField(blank=True, null=True)
    Level = models.IntegerField(blank=True, null=True)
    CS = models.IntegerField(blank=True, null=True)
    MatchId = models.ForeignKey(MatchData, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
