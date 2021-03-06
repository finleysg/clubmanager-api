from django.conf.urls import url
from django.views.decorators.cache import cache_page

from core import views as core_views
from courses import views as course_views
from events import views as event_views
from policies import views as policy_views
from register import views as register_views
from messaging import views as messaging_views
from documents import views as document_views


urlpatterns = [
    url(r'^$', core_views.api_root),
    url(r'^stripe/details/$', core_views.stripe_details, name='stripe-details'),
    url(r'^stripe/card/$', core_views.save_card, name='save-card'),
    url(r'^settings/$', core_views.current_settings, name='current-settings'),
    url(r'^members/$', cache_page(60 * 10)(core_views.MemberList.as_view()), name='member-list'),
    url(r'^members/(?P<pk>[0-9]+)/$', core_views.MemberDetail.as_view(), name='member-detail'),
    url(r'^members/charges/$', core_views.stripe_charges, name='member-charges'),
    url(r'^members/check/$', core_views.is_available, name='is-available'),
    url(r'^members/register/$', core_views.register_new_member, name='register-member'),
    url(r'^courses/$', course_views.CourseList.as_view(), name='course-list'),
    url(r'^courses/(?P<pk>[0-9]+)/$', course_views.CourseDetail.as_view(), name='course-detail'),
    url(r'^course-setups/$', course_views.CourseSetupList.as_view(), name='coursesetup-list'),
    url(r'^course-setups/(?P<pk>[0-9]+)/$', course_views.CourseSetupDetail.as_view(), name='coursesetup-detail'),
    url(r'^holes/$', course_views.HoleList.as_view(), name='hole-list'),
    url(r'^holes/(?P<pk>[0-9]+)/$', course_views.HoleDetail.as_view(), name='hole-detail'),
    url(r'^course-setup-holes/$', course_views.CourseSetupHoleList.as_view(), name='coursesetuphole-list'),
    url(r'^course-setup-holes/(?P<pk>[0-9]+)/$', course_views.CourseSetupHoleDetail.as_view(), name='coursesetuphole-detail'),
    url(r'^events/$', cache_page(60 * 10)(event_views.EventList.as_view()), name='event-list'),
    url(r'^events/current/$', cache_page(60 * 60)(event_views.QuickEventList.as_view()), name='quick-event-list'),
    url(r'^events/upcoming/$', event_views.UpcomingEventList.as_view(), name='upcoming-event-list'),
    url(r'^events/(?P<pk>[0-9]+)/$', event_views.EventDetail.as_view(), name='event-detail'),
    url(r'^events/(?P<pk>[0-9]+)/portal/$', event_views.update_portal, name='event-portal'),
    url(r'^event-templates/$', event_views.EventTemplateList.as_view(), name='eventtemplate-list'),
    url(r'^event-templates/(?P<pk>[0-9]+)/$', event_views.EventTemplateDetail.as_view(), name='eventtemplate-detail'),
    url(r'^documents/$', document_views.DocumentList.as_view(), name='document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', document_views.DocumentDetail.as_view(), name='document-detail'),
    url(r'^photos/$', document_views.PhotoList.as_view(), name='photo-list'),
    url(r'^photos/(?P<pk>[0-9]+)/$', document_views.PhotoDetail.as_view(), name='photo-detail'),
    url(r'^announcements/$', messaging_views.AnnouncementList.as_view(), name='announcement-list'),
    url(r'^announcements/(?P<pk>[0-9]+)/$', messaging_views.AnnouncementDetail.as_view(), name='announcement-detail'),
    url(r'^policies/$', cache_page(60 * 15)(policy_views.PolicyList.as_view()), name='policy-list'),
    url(r'^policies/(?P<pk>[0-9]+)/$', policy_views.PolicyDetail.as_view(), name='policy-detail'),
    url(r'^sponsors/$', cache_page(60 * 120)(document_views.SponsorList.as_view()), name='sponsor-list'),
    url(r'^registrations/$', register_views.RegistrationList.as_view(), name='registration-list'),
    url(r'^registrations/(?P<pk>[0-9]+)/$', register_views.RegistrationDetail.as_view(), name='registration-detail'),
    url(r'^registration/(?P<event_id>[0-9]+)/(?P<member_id>[0-9]+)/$', register_views.is_registered, name='registration-check'),
    url(r'^registration/groups/$', register_views.RegistrationGroupList.as_view(), name='registration-group-list'),
    url(r'^registration/groups/(?P<pk>[0-9]+)/$', register_views.RegistrationGroupDetail.as_view(), name='registration-group'),
    url(r'^registration/charge/$', register_views.get_charge, name='registration-charge'),
    url(r'^registration/charges/(?P<event_id>[0-9]+)/$', register_views.get_charges, name='registration-charges'),
    url(r'^registration/reserve/$', register_views.reserve, name='reserve'),
    url(r'^registration/register/$', register_views.register, name='register'),
    url(r'^registration/drop/$', register_views.drop, name='drop-registration'),
    url(r'^registration/move/$', register_views.move, name='move-registration'),
    url(r'^registration/cancel/$', register_views.cancel_reserved_slots, name='cancel-reserved-slots'),
    url(r'^registration/add-groups/$', register_views.add_groups, name='add-groups'),
    # url(r'^registration/remove-row/$', register_views.remove_row, name='remove-row'),
    url(r'^registration/slot-payments/$', register_views.RegistrationSlotPaymentList.as_view(), name='registration-slot-payments'),
    url(r'^registration/slot-payments/(?P<pk>[0-9]+)/$', register_views.RegistrationSlotPaymentDetail.as_view(), name='registration-slot-payment'),
    url(r'^contact-us/$', messaging_views.contact_message, name='contact-us'),
    url(r'^contacts/$', messaging_views.ContactList.as_view(), name='contact-list'),
    url(r'^friends/$', core_views.friends, name='friends'),
    url(r'^friends/add/(?P<member_id>[0-9]+)/$', core_views.add_friend, name='add_friend'),
    url(r'^friends/remove/(?P<member_id>[0-9]+)/$', core_views.remove_friend, name='remove_friend'),
]
