"""
Admin configuration for managing CinemaUser and
SpectatorProfile objects in the Django admin panel.
"""

from django.contrib import admin

from .models import CinemaUser, SpectatorProfile
from .forms import AdminCinemaUserForm


@admin.register(CinemaUser)
class CinemaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CinemaUser model.
    Allows creating and managing administrator users.
    """
    form = AdminCinemaUserForm
    list_display = ('username', 'role', 'is_staff', 'is_superuser')
    list_display_links = ('username',)
    list_filter = ('role',)
    list_per_page = 15
    search_fields = ('username', 'role')
    ordering = ('-is_superuser', '-is_staff', 'role')


@admin.register(SpectatorProfile)
class SpectatorProfileAdmin(admin.ModelAdmin):
    """
    Admin class for managing SpectatorProfile objects in the Django admin panel.
    """
    list_display = ('user', 'full_name', 'account')
    list_per_page = 15
    search_fields = ('user',)
    readonly_fields = ('user', 'full_name', 'account')

    @staticmethod
    def full_name(obj):
        """
        Custom method to display the full name of the user.
        """
        return f"{obj.user.first_name} {obj.user.last_name}"

    def has_add_permission(self, request):
        """
        Prevent adding new SpectatorProfile objects from the admin panel.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting SpectatorProfile objects from the admin panel.
        """
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Customized the change view for SpectatorProfile objects.
        Hide the save buttons to prevent saving changes.
        """
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
