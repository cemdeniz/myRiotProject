from django import forms
from django.forms import TextInput


class LolForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    region = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Region', 'style': 'width: 300px;', 'class': 'form-control'}))
