from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.LolView.as_view(), name='LolView'),
    path('profile/<sumName>/<region>', views.profile, name='profile'),
    path('matchdetail/<myName>/<matchId>', views.matchdetail, name='matchdetail')

]


