from django import forms
from django.forms import TextInput
from .models import Player, Summoner


class LolForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    region = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Region', 'style': 'width: 300px;', 'class': 'form-control'}))


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['sname', 'region', 'email', 'passwd']


class SummonerForm(forms.ModelForm):
    class Meta:
        model = Summoner
        fields = ['sname', 'region', 'level', 'tier', 'rank', 'lp', 'win', 'lose']
