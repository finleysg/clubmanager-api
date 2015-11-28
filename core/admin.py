from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Member, Club
from events.models import Event, EventTemplate


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (MemberInline, )


class ClubAdmin(admin.ModelAdmin):
    fields = ['description', 'address1', 'address2', 'city', 'state', 'zip', 'website', 'contact_email', 'phone_number']


class EventTemplateAdmin(admin.ModelAdmin):
    fields = ['name','description','rounds','holes_per_round','event_fee','skins_fee','minimum_signup_group_size',
              'maximum_signup_group_size','group_size','is_shotgun_start','can_signup_group','can_choose_hole',
              'scoring','scoring_system','team_scoring','number_of_scores']


class EventAdmin(admin.ModelAdmin):
    fields = ['name','description', 'courses', 'start_date', 'start_time', 'signup_start', 'signup_end',
              'rounds','holes_per_round','event_fee','skins_fee','minimum_signup_group_size',
              'maximum_signup_group_size','group_size','is_shotgun_start','can_signup_group','can_choose_hole',
              'scoring','scoring_system','team_scoring','number_of_scores']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTemplate, EventTemplateAdmin)
