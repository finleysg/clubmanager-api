from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from core.models import SeasonSettings
from events.models import Event
from .models import RegistrationGroup, RegistrationSlot

config = SeasonSettings.objects.current_settings()


class NoLeagueFilter(SimpleListFilter):
    title = '{} events'.format(config.year)
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        events = set([c for c in Event.objects.filter(start_date__year=config.year).filter(requires_registration=True).exclude(event_type='L')])
        return [(e.id, e.name) for e in events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event__id__exact=self.value())
        else:
            return queryset


class RegistrationSlotInline(admin.TabularInline):
    model = RegistrationSlot
    can_delete = True
    extra = 0
    verbose_name_plural = 'Signed up'
    fields = ["member", "is_event_fee_paid", "is_gross_skins_paid", "is_net_skins_paid", "is_greens_fee_paid",
              "is_cart_fee_paid", ]


class RegistrationGroupAdmin(admin.ModelAdmin):
    model: RegistrationGroup
    can_delete = True
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('event', 'signed_up_by', ), )
        }),
        ('Payment Information', {
            'fields': ('payment_amount', 'payment_confirmation_code', 'payment_confirmation_timestamp', )
        }),
        ('Notes', {
            'fields': ('notes', )
        })
    )
    inlines = [RegistrationSlotInline, ]

    list_display = ['members', 'payment_confirmation_code', 'payment_confirmation_timestamp', 'event', ]
    list_display_links = ('members', )
    list_filter = (NoLeagueFilter, )

    # def members(self, obj):
    #     member_names = []
    #     for slot in obj.slots.all():
    #         member_names.append(slot.member.member_name())
    #     return ", ".join(member_names)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event":
            kwargs["queryset"] = Event.objects.filter(start_date__year=config.year).filter(requires_registration=True).exclude(event_type='L')
        return super(RegistrationGroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['signed_up_by'] = request.user.member.id
        if '_changelist_filters' in request.GET:
            filters = request.GET['_changelist_filters']
            initial['event'] = filters.split('=')[1]
        return initial

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event_id = instance.registration_group.event_id
            instance.save()
        formset.save_m2m()

admin.site.register(RegistrationGroup, RegistrationGroupAdmin)