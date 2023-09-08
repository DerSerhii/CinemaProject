from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from ..admin import CinemaAdmin, SpectatorProfileAdmin
from ..models import CinemaUser, SpectatorProfile


User = get_user_model()


class CinemaAdminTestCase(TestCase):
    """
    Test cases for `:class:CinemaAdmin` in the admin module.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = AdminSite()
        self.superuser = User.objects.create_superuser(username='admin', password='admin123')
        self.cinema_admin = CinemaAdmin(CinemaUser, self.admin_site)
        self.spectator_profile_admin = SpectatorProfileAdmin(SpectatorProfile, self.admin_site)

    def test_cinema_admin_list_display(self):
        """
        Test whether the `list_display` attribute of CinemaAdmin is correctly configured.
        """
        expected_list_display = ('username', 'role', 'is_staff', 'is_superuser')
        self.assertEqual(expected_list_display, CinemaAdmin.list_display)

    def test_cinema_admin_access_list(self):
        """
        Test if an admin user can access the user list page in the admin panel.
        """
        url = reverse('admin:cinema_admin_cinemauser_changelist')

        request = self.factory.get(url)
        request.user = self.superuser
        response = self.cinema_admin.changelist_view(request)
        self.assertEqual(200, response.status_code)

    def test_cinema_admin_create_user(self):
        """
        Test checks access to the page for creating a new user in the Django admin panel.
        """
        url = reverse('admin:cinema_admin_cinemauser_add')
        request = self.factory.get(url)
        request.user = self.superuser
        response = self.cinema_admin.add_view(request)
        self.assertEqual(200, response.status_code)

    def test_cinema_admin_edit_user(self):
        """
        Test checks access to the page for editing an existing user in the Django admin panel.
        """
        user = CinemaUser.objects.create_user(username='test_user', password='test123')
        url = reverse('admin:cinema_admin_cinemauser_change', args=[user.id])
        request = self.factory.get(url)
        request.user = self.superuser
        response = self.cinema_admin.change_view(request, str(user.id))
        self.assertEqual(200, response.status_code)

    def test_cinema_admin_delete_user(self):
        """
        Test checks access to the page for deleting an existing user in the Django admin panel.
        """
        user = CinemaUser.objects.create_user(username='test_user', password='test123')
        url = reverse('admin:cinema_admin_cinemauser_delete', args=[user.id])
        request = self.factory.get(url)
        request.user = self.superuser
        response = self.cinema_admin.delete_view(request, str(user.id))
        self.assertEqual(200, response.status_code)


class SpectatorProfileAdminTestCase(TestCase):
    """
    Test cases for `:class:CinemaAdmin` in the admin module.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = AdminSite()
        self.user = User.objects.create_superuser(username='admin', password='admin123')
        self.spectator_profile_admin = SpectatorProfileAdmin(SpectatorProfile, self.admin_site)

    def test_spectator_profile_admin_list_display(self):
        """
        Test whether the `list_display` attribute of SpectatorProfileAdmin is correctly configured.
        """
        self.assertEqual(SpectatorProfileAdmin.list_display, ('user', 'full_name', 'account'))
