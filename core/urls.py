from django.conf.urls import url
from core import views as core_views
from courses import views as course_views
from events import views as event_views
from policies import views as policy_views
from signup import views as signup_views
from payments import views as payment_views
from messaging import views as messaging_views
from documents import views as document_views


urlpatterns = [
    url(r'^$', core_views.api_root),
    url(r'^settings/$', core_views.global_settings, name='settings'),
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
    url(r'^documents/$', document_views.DocumentList.as_view(), name='document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', document_views.DocumentDetail.as_view(), name='document-detail'),
    url(r'^announcements/$', messaging_views.AnnouncementList.as_view(), name='announcement-list'),
    url(r'^announcements/(?P<pk>[0-9]+)/$', messaging_views.AnnouncementDetail.as_view(), name='announcement-detail'),
    url(r'^policies/$', policy_views.PolicyList.as_view(), name='policy-list'),
    url(r'^policies/(?P<pk>[0-9]+)/$', policy_views.PolicyDetail.as_view(), name='policy-detail'),
    url(r'^registrations/(?P<event_id>[0-9]+)/$', signup_views.registrations, name='registrations'),
    url(r'^registration/slots/(?P<event_id>[0-9]+)/$', signup_views.registration_slots, name='registration-slots'),
    url(r'^registration/reserve/$', signup_views.reserve_slots, name='reserve-slots'),
    url(r'^registration/register/$', signup_views.register, name='register'),
    url(r'^registration/cancel/$', signup_views.cancel_reserved_slots, name='cancel-reserved-slots'),
    url(r'^registration/pay/$', payment_views.pay, name='pay'),
    url(r'^friends/$', core_views.friends, name='friends'),
]
