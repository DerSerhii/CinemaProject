from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CinemaUser, SpectatorProfile
from .forms import AdminCinemaUserForm


@admin.register(CinemaUser)
class CinemaAdmin(admin.ModelAdmin):
    form = AdminCinemaUserForm
    list_display = ['username', 'role', 'is_staff', 'is_superuser']
    list_display_links = ['username']
    list_filter = ['role']
    list_per_page = 15
    search_fields = ['username', 'role']
    ordering = ['-is_superuser', '-is_staff', 'role']


@admin.register(SpectatorProfile)
class SpectatorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'account']

    @staticmethod
    def full_name(obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def has_add_permission(self, request):
        return False
