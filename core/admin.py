from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Member, SeasonSettings


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'
    fields = ["ghin", "birth_date", "forward_tees", 'address1', 'city', 'state', 'zip', 'phone_number', 'stripe_customer_id']


# Define a new User admin
class BhmcUserAdmin(UserAdmin):
    inlines = (MemberInline, )
    list_display = ["email", "first_name", "last_name", "is_active", ]
    list_editable = ["is_active", ]
    save_on_top = True


class ClubAdmin(admin.ModelAdmin):
    fields = ['description', 'address1', 'address2', 'city', 'state', 'zip', 'website', 'contact_email', 'phone_number']


class SettingsAdmin(admin.ModelAdmin):
    fields = ['year', 'reg_event', 'match_play_event', 'accept_new_members', ]
    list_display = ['year', ]
    can_delete = False

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, BhmcUserAdmin)
admin.site.register(SeasonSettings, SettingsAdmin)
# admin.site.register(Club, ClubAdmin)
