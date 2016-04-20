from django.conf.urls import url
from core import views as core_views
from courses import views as course_views
from events import views as event_views

urlpatterns = [
    url(r'^$', core_views.api_root),
    url(r'^clubs/$', core_views.ClubList.as_view(), name='club-list'),
    url(r'^clubs/(?P<pk>[0-9]+)/$', core_views.ClubDetail.as_view(), name='club-detail'),
    url(r'^members/$', core_views.MemberList.as_view(), name='member-list'),
    url(r'^members/(?P<pk>[0-9]+)/$', core_views.MemberDetail.as_view(), name='member-detail'),
    url(r'^courses/$', course_views.CourseList.as_view(), name='course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$', course_views.CourseDetail.as_view(), name='course-detail'),
    url(r'^course-setups/$', course_views.CourseSetupList.as_view(), name='coursesetup-list'),
    url(r'^course-setups/(?P<pk>[0-9]+)/$', course_views.CourseSetupDetail.as_view(), name='coursesetup-detail'),
    url(r'^holes/$', course_views.HoleList.as_view(), name='hole-list'),
    url(r'^holes/(?P<pk>[0-9]+)/$', course_views.HoleDetail.as_view(), name='hole-detail'),
    url(r'^course-setup-holes/$', course_views.CourseSetupHoleList.as_view(), name='coursesetuphole-list'),
    url(r'^course-setup-holes/(?P<pk>[0-9]+)/$', course_views.CourseSetupHoleDetail.as_view(), name='coursesetuphole-detail'),
    url(r'^events/$', event_views.EventList.as_view(), name='event-list'),
    url(r'^upcoming-events/$', event_views.UpcomingEventList.as_view(), name='upcoming-event-list'),
    url(r'^events/(?P<pk>[0-9]+)/$', event_views.EventDetail.as_view(), name='event-detail'),
    url(r'^event-templates/$', event_views.EventTemplateList.as_view(), name='eventtemplate-list'),
    url(r'^event-templates/(?P<pk>[0-9]+)/$', event_views.EventTemplateDetail.as_view(), name='eventtemplate-detail'),
]