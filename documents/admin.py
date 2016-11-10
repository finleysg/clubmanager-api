from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    fields = ['document_type', 'event', 'title', 'file', ]
    list_display = ['title', 'document_type', ]
    list_filter = ('document_type', )
    save_on_top = True

admin.site.register(Document, DocumentAdmin)

