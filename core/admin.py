from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Member, Club


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (MemberInline, )
    save_on_top = True

class ClubAdmin(admin.ModelAdmin):
    fields = ['description', 'address1', 'address2', 'city', 'state', 'zip', 'website', 'contact_email', 'phone_number']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Club, ClubAdmin)
