from django.contrib.auth.models import User
from django.db import models
from django.forms import TextInput, ModelForm
from django.utils import timezone
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Player(models.Model):
    sname = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, null=True)
    passwd = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.sname + ' / ' + self.region


class Summoner(models.Model):
    sname = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    tier = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    lp = models.CharField(max_length=50)
    win = models.CharField(max_length=50)
    lose = models.CharField(max_length=50)
    veteran = models.CharField(max_length=50)
    inactive = models.CharField(max_length=50)
    fblood = models.CharField(max_length=50)
    hstreak = models.CharField(max_length=50)
    lastMatch = models.CharField(max_length=50)

    def __str__(self):
        return self.sname + ' / ' + self.region
