from django.contrib import admin
from .models import Event, EventTemplate
from signup.models import SignupSlot


class EventTemplateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', ('event_type', 'requires_registration', 'start_type'), ('rounds', 'holes_per_round'), ('event_fee', 'skins_fee', 'skins_type'),)
        }),
        ('Format, Rules, and Notes', {
            'classes': ('wide',),
            'fields': ('description', 'notes',)
        }),
        ('Signup Behavior', {
            'fields': (('minimum_signup_group_size', 'maximum_signup_group_size', 'group_size'), ('can_signup_group', 'can_choose_hole'),)
        }),
        ('Scoring', {
            'fields': ('season_points', ('scoring', 'scoring_system', 'number_of_scores'),)
        }),
        ('Other', {
            'fields': ('external_url',)
        })
    )

    def event_type_display(self, obj):
        return obj.get_event_type_display()
    event_type_display.short_description = "Event Type"

    list_display = ['event_type_display', 'name']
    list_display_links = ('name',)


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('template',)
        }),
        ('Basic Settings and Fees', {
            'fields': ('name', ('event_type', 'requires_registration', 'start_type'), ('rounds', 'holes_per_round'), ('event_fee', 'skins_fee', 'skins_type'),)
        }),
        ('Format, Rules, and Notes', {
            'classes': ('wide',),
            'fields': ('description', 'notes',)
        }),
        ('Signup Behavior', {
            'fields': (('registration_maximum', 'minimum_signup_group_size', 'maximum_signup_group_size', 'group_size'), ('can_signup_group', 'can_choose_hole'),)
        }),
        ('Scoring', {
            'fields': ('season_points', ('scoring', 'scoring_system', 'number_of_scores'),)
        }),
        ('Dates and Times', {
            'fields': (('start_date', 'start_time'), ('end_date', 'end_time'), ('signup_start', 'signup_end'))
        }),
        ('Courses', {
            'fields': ('course_setups',)
        }),
        ('Other', {
            'fields': ('external_url',)
        })
    )

    def save_model(self, request, obj, form, change):
        # obj.save()
        super(EventAdmin, self).save_model(request, obj, form, change)

        # TODO: don't do this after registration has begun
        SignupSlot.objects.clear_slots(obj)
        SignupSlot.objects.create_slots(obj)

    def event_type_display(self, obj):
        return obj.get_event_type_display()

    event_type_display.short_description = "Event Type"
    list_display = ['name', 'start_date', 'event_type_display']
    list_display_links = ('name',)
    ordering = ['start_date']


admin.site.register(Event, EventAdmin)
admin.site.register(EventTemplate, EventTemplateAdmin)
