from django.contrib import admin
from .models import Announcement


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

