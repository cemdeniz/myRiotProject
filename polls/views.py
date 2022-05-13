import gettext

import form as form
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView
from riotwatcher import LolWatcher
from .forms import LolForm, PlayerForm
from .models import Player
from django.contrib import messages
import requests

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def signup(request):
    return render(request, 'polls/signup.html', {})


def home(request):
    if request.method == "POST":
        form = PlayerForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            sname = request.POST['sname']
            region = request.POST['region']
            email = request.POST['email']
            passwd = request.POST['passwd']
            messages.success(request, "Player did not saved!")
            # return redirect('polls/home.html')
            return render(request, 'polls/signup.html',
                          {'sname': sname, 'region': region, 'email': email, 'passwd': passwd})
        messages.success(request, "Player saved Successfully!")
        return redirect('LolView')
    else:
        return render(request, 'polls/signup.html', {})


class LolView(TemplateView):
    # lol_watcher = LolWatcher('RGAPI-ca6bcefe-3277-45e0-bb0b-29779724ea15')
    template_name = 'polls/home.html'

    def get(self, request):
        all_players = Player.objects.all
        form = LolForm()
        return render(request, self.template_name, {'form': form, 'all_players': all_players})

    def post(self, request):
        form = LolForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            region = form.cleaned_data['region']
            form = LolForm
            lol_watcher = LolWatcher('RGAPI-5ae835e4-48e2-40dd-b393-ef6b133f9f81')

            me = lol_watcher.summoner.by_name(region, name)
            my_ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
            my_matches = lol_watcher.match.matchlist_by_puuid('europe', me['puuid'])
            #print("me", me)
            print("my_ranked_stats: ", my_ranked_stats)
            wrPerc = int(my_ranked_stats[1]['wins'] / (my_ranked_stats[1]['wins'] + my_ranked_stats[1]['losses']) * 100)
            icon = lol_watcher.data_dragon.profile_icons(version="12.7.1")

            # print("my matches: ", my_matches)

            myLastMatches = []
            freeChampionsIds = []
            freeChampionsForNew = []
            first_team = []
            second_team = []

            for x in range(16):
                freeChampionsIds.append(lol_watcher.champion.rotations('tr1')['freeChampionIds'][x])
            champions = lol_watcher.data_dragon.champions('12.7.1')

            for x in range(10):
                freeChampionsForNew.append(lol_watcher.champion.rotations('tr1')['freeChampionIdsForNewPlayers'][x])

            for x in range(5):
                myLastMatches.append(my_matches[x])
            lastMatchDetail = lol_watcher.match.by_id('europe', myLastMatches[0])

            for x in range(5):
                first_team.append(lastMatchDetail['info']['participants'][x]['summonerName'])
            for x in range(5, 10):
                second_team.append(lastMatchDetail['info']['participants'][x]['summonerName'])

            first_team_kda = []
            first_team_level = []
            first_team_gold = []
            first_team_soloKills = []
            first_team_champName = []
            first_team_mythicItemUsed = []
            second_team_kda = []
            second_team_level = []
            second_team_gold = []
            second_team_soloKills = []
            second_team_champName = []
            second_team_mythicItemUsed = []

            for x in range(5):
                first_team_kda.append(round(lastMatchDetail['info']['participants'][x]['challenges']['kda'], 2))
            for x in range(5, 10):
                second_team_kda.append(round(lastMatchDetail['info']['participants'][x]['challenges']['kda'], 2))

            for x in range(5):
                first_team_level.append(lastMatchDetail['info']['participants'][x]['champLevel'])
            for x in range(5, 10):
                second_team_level.append(lastMatchDetail['info']['participants'][x]['champLevel'])

            for x in range(5):
                first_team_gold.append(lastMatchDetail['info']['participants'][x]['goldEarned'])
            for x in range(5, 10):
                second_team_gold.append(lastMatchDetail['info']['participants'][x]['goldEarned'])

            for x in range(5):
                first_team_soloKills.append(lastMatchDetail['info']['participants'][x]['challenges']['soloKills'])
            for x in range(5, 10):
                second_team_soloKills.append(lastMatchDetail['info']['participants'][x]['challenges']['soloKills'])

            for x in range(5):
                first_team_champName.append(lastMatchDetail['info']['participants'][x]['championName'])
            for x in range(5, 10):
                second_team_champName.append(lastMatchDetail['info']['participants'][x]['championName'])

            gameDuration = lastMatchDetail['info']['gameDuration']
            gameMin = int(gameDuration / 60)
            gameSec = int(gameDuration % 60)
            gameMode = lastMatchDetail['info']['gameMode']

            #print("test: ", lastMatchDetail['info']['participants'][0])

        args = {'form': form,
                'sumName': me['name'],
                'sumLevel': me['summonerLevel'],
                'freeChampions': freeChampionsIds,
                'freeChampionsForNew': freeChampionsForNew,
                'veteran': my_ranked_stats[0]['veteran'],
                'inactive': my_ranked_stats[0]['inactive'],
                'freshBlood': my_ranked_stats[0]['freshBlood'],
                'hotStreak': my_ranked_stats[0]['hotStreak'],
                'queueType': my_ranked_stats[1]['queueType'],
                'tier': my_ranked_stats[1]['tier'],
                'rank': my_ranked_stats[1]['rank'],
                'leaguePoints': my_ranked_stats[1]['leaguePoints'],
                'winNumber': my_ranked_stats[1]['wins'],
                'loseNumber': my_ranked_stats[1]['losses'],
                'wrPerc': wrPerc,
                'myLastMatches': myLastMatches,
                'gameId': lastMatchDetail['info']['gameId'],
                'first_team': first_team,
                'second_team': second_team,
                'first_team_kda': first_team_kda,
                'first_team_level': first_team_level,
                'first_team_gold': first_team_gold,
                'first_team_soloKills': first_team_soloKills,
                'first_team_champName': first_team_champName,
                'first_team_mythicItemUsed': first_team_mythicItemUsed,
                'second_team_kda': second_team_kda,
                'second_team_level': second_team_level,
                'second_team_gold': second_team_gold,
                'second_team_soloKills': second_team_soloKills,
                'second_team_champName': second_team_champName,
                'second_team_mythicItemUsed': second_team_mythicItemUsed,
                'gameMode': gameMode,
                'gameMin': gameMin,
                'gameSec': gameSec,
                'myRole': lastMatchDetail['info']['participants'][0]['individualPosition'],
                'lastChampion': lastMatchDetail['info']['participants'][0]['championName'],
                'lastWinLose': lastMatchDetail['info']['participants'][0]['win'],
                'my_icon_id': 'https://static.senpai.gg/lol/img/profileicon/{}.png'.format(me['profileIconId'])}
        return render(request, 'polls/lol.html', args)
