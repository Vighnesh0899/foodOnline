from django.contrib import admin
from accounts.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class customUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal=()
    list_filter= ()
    fieldsets=()

admin.site.register(User, customUserAdmin)
admin.site.register(UserProfile)
