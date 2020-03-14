from django.contrib import admin
from .models import Announcement, ContactMessage, Contact


class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("title", "text", "starts", "expires", "visibility", )
        }),
        ("Link to an event or document (optional)", {
            "fields": ("event", "document", )
        }),
        ("Link to an external site (optional)", {
            "fields": ("external_url", "external_name", )
        }),
    )
    list_display = ["starts", "expires", "title", ]
    list_filter = ("starts", )
    save_on_top = True


admin.site.register(Announcement, AnnouncementAdmin)


class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Officers", {
            "fields": ("president_name", "president_phone", "vice_president_name", "vice_president_phone",
                       "secretary_name", "secretary_phone", "treasurer_name", "treasurer_phone", )
        }),
        (None, {
            "fields": ("directors", "committees", "staff", )
        })
    )
    save_on_top = True


admin.site.register(Contact, ContactAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("full_name", "email", )
        }),
        ("Message", {
            "fields": ("message_text", )
        }),
    )
    list_display = ["full_name", "message_date", ]
    list_filter = ("message_date", )
    save_on_top = True


admin.site.register(ContactMessage, ContactMessageAdmin)
