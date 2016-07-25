from django.contrib import admin
from roles.models import Role, RoleMember


class RoleAdmin(admin.ModelAdmin):
    fields = ['role_type', 'title', 'description', ]


class RoleMemberAdmin(admin.ModelAdmin):
    fields = ['role', 'member', 'expires', 'is_chair', 'is_officer']

admin.site.register(Role, RoleAdmin)
admin.site.register(RoleMember, RoleMemberAdmin)

