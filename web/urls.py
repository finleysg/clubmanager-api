from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'account/', views.account, name='account'),
    url(r'calendar/', views.calendar, name='calendar'),
    url(r'contact/', views.contact, name='contact'),
    url(r'dam-cup/', views.dam_cup, name='dam-cup'),
    url(r'directory/', views.directory, name='directory'),
    url(r'event-detail/', views.event_detail, name='event-detail'),
    url(r'forum/', views.forum, name='forum'),
    url(r'league-results/', views.league_results, name='league-results'),
    url(r'local-rules/', views.local_rules, name='local-rules'),
    url(r'major-results/', views.major_results, name='major-results'),
    url(r'policies/', views.policies, name='policies'),
    url(r'profile/', views.profile, name='profile'),
    url(r'register/', views.register, name='register'),
    url(r'results/', views.results, name='results'),
    url(r'slp/', views.season_long_points, name='slp'),
]
