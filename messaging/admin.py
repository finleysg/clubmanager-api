from django.contrib import admin
from .models import Announcement, ContactMessage


class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("text", "starts", "expires", )
        }),
        ("Link (optional)", {
            "fields": ("event", "event_link_type", "document", "external_url", "external_name", )
        }),
    )
    list_display = ["starts", "expires", "short_text", ]
    list_filter = ("starts", )
    save_on_top = True

admin.site.register(Announcement, AnnouncementAdmin)


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
