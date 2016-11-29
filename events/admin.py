from django.contrib import admin
from .models import Event, EventTemplate
from register.models import SignupSlot


class EventTemplateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', ('event_type', 'start_type'), ('rounds', 'holes_per_round'), ('event_fee', 'skins_fee', 'skins_type'),)
        }),
        ('Format, Rules, and Notes', {
            'classes': ('wide',),
            'fields': ('description', 'notes',)
        }),
        ('Registration', {
            'fields': ('requires_registration', ('minimum_signup_group_size', 'maximum_signup_group_size', 'group_size'), ('can_signup_group', 'can_choose_hole'),)
        }),
        ('Other', {
            'fields': ('season_points', 'external_url',)
        })
    )

    def event_type_display(self, obj):
        return obj.get_event_type_display()
    event_type_display.short_description = "Event Type"

    list_display = ['event_type_display', 'name']
    list_display_links = ('name',)
    list_filter = ("event_type", )
    save_on_top = True


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('template',)
        }),
        ('Basic Settings and Fees', {
            'fields': ('name', ('event_type', 'start_type'), ('rounds', 'holes_per_round'), ('event_fee', 'skins_fee', 'skins_type'),)
        }),
        ('Format, Rules, and Notes', {
            'classes': ('wide',),
            'fields': ('description', 'notes',)
        }),
        ('Event Date', {
            'fields': ('start_date', 'start_time', )
        }),
        ('Registration', {
            'fields': ('requires_registration', ('signup_start', 'signup_end'), ('registration_maximum', 'minimum_signup_group_size', 'maximum_signup_group_size', 'group_size'), ('can_signup_group', 'can_choose_hole'),)
        }),
        ('Other', {
            'fields': ('season_points', 'external_url',)
        }),
        ('Courses', {
            'fields': ('course_setups',)
        }),
    )

    def save_model(self, request, obj, form, change):
        super(EventAdmin, self).save_model(request, obj, form, change)

        if obj.registration_window() == "future" and obj.group_size > 1 and obj.can_signup_group:
            SignupSlot.objects.remove_slots(obj)
            SignupSlot.objects.create_slots(obj)

    def event_type_display(self, obj):
        return obj.get_event_type_display()

    event_type_display.short_description = "Event Type"
    list_display = ['name', 'start_date', 'event_type_display']
    list_display_links = ('name',)
    list_filter = ("start_date", "event_type")
    ordering = ['start_date']
    save_on_top = True


admin.site.register(Event, EventAdmin)
admin.site.register(EventTemplate, EventTemplateAdmin)
