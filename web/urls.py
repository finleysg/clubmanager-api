from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^loaderio-c54279d9d52133c06541d1471217c18b/$', views.index, name='load-test'),
    # url(r'account/', views.account, name='account'),
    # url(r'calendar/', views.calendar, name='calendar'),
    # url(r'contact/', views.contact, name='contact'),
    # url(r'dam-cup/', views.dam_cup, name='dam-cup'),
    # url(r'directory/', views.directory, name='directory'),
    # url(r'event/(?P<event_id>[0-9]+)/$', views.event_detail, name='event-detail'),
    # url(r'event/(?P<event_id>[0-9]+)/register/$', views.register, name='register'),
    # url(r'event/(?P<event_id>[0-9]+)/results/$', views.results, name='results'),
    # url(r'event/(?P<event_id>[0-9]+)/teetimes/$', views.teetimes, name='teetimes'),
    # url(r'forum/', views.forum, name='forum'),
    # url(r'league-results/', views.league_results, name='league-results'),
    # url(r'local-rules/', views.local_rules, name='local-rules'),
    # url(r'major-results/', views.major_results, name='major-results'),
    # url(r'match-play/', views.match_play, name='match-play'),
    # # url(r'policies/', views.policies, name='policies'),
    # url(r'profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    # url(r'profile_default/', views.profile_default, name='profile_default'),
    # url(r'season-long-points/', views.season_long_points, name='season-long-points'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

