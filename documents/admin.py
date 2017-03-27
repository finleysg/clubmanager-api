from django.contrib import admin
from .models import Document, Sponsor


class DocumentAdmin(admin.ModelAdmin):
    fields = ['year', 'document_type', 'event', 'title', 'file', ]
    list_display = ['year', 'title', 'document_type', ]
    list_filter = ('year', 'document_type', )
    save_on_top = True


class SponsorAdmin(admin.ModelAdmin):
    fields = ["name", "description", "website", "level", "ad_image", ]
    list_display = ['name', 'level', 'website', ]
    save_on_top = True

admin.site.register(Document, DocumentAdmin)
admin.site.register(Sponsor, SponsorAdmin)
