from django.contrib import admin
from .models import Announcement, ContactMessage


class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("title", "text", "starts", "expires", "members_only", )
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
