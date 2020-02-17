from django.contrib import admin
from .models import Document, Sponsor, Photo


class DocumentAdmin(admin.ModelAdmin):
    fields = ['year', 'document_type', 'event', 'title', 'file', 'display_flag', ]
    list_display = ['year', 'title', 'document_type', ]
    list_filter = ('year', 'document_type', )
    date_hierarchy = "last_update"
    save_on_top = True


class PhotoAdmin(admin.ModelAdmin):
    fields = ['year', 'photo_type', 'event', 'title', 'file', ]
    list_display = ['year', 'title', 'photo_type', ]
    list_filter = ('year', 'photo_type', )
    date_hierarchy = "last_update"
    save_on_top = True


class SponsorAdmin(admin.ModelAdmin):
    fields = ["name", "description", "website", "level", "ad_image", ]
    list_display = ['name', 'level', 'website', ]
    save_on_top = True


admin.site.register(Document, DocumentAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Sponsor, SponsorAdmin)
