"""
The module represents test cases for models of module `models`.
"""

from multiprocessing import Process

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import TestCase

from ..models import UserRole, CinemaUser, SpectatorProfile


class CinemaUserModelTestCase(TestCase):
    """
    Test case for the model `:class:UserRole`.
    """

    def setUp(self):
        # Create a test superuser
        self.superuser = CinemaUser.objects.create_superuser(
            username='admin', password='admin_pass'
        )

    def test_superuser_role(self):
        """
        Superuser is automatically assigned the role `Administrator`.
        """
        expected_role_for_superuser = UserRole.ADMIN
        self.assertEqual(expected_role_for_superuser, self.superuser.role)

    def test_create_spectator_user(self):
        """
        By default, `CinemaUser` should be given `Spectator` role in cinema system.
        Users with `Spectator` role automatically get Spectator Profile.
        """
        spectator_user = CinemaUser.objects.create(
            username='spectator', password='spectator_pass'
        )
        expected_role_by_default = UserRole.SPECTATOR
        self.assertEqual(expected_role_by_default, spectator_user.role)
        self.assertTrue(hasattr(spectator_user, 'profile'))
        self.assertIsInstance(spectator_user.profile, SpectatorProfile)

    def test_create_staff_user(self):
        """
        Staff is automatically assigned the role `Administrator`.
        """
        staff_user = CinemaUser.objects.create(
            username='staff', password='staff_pass', is_staff=True
        )
        expected_role_for_staff = UserRole.ADMIN
        self.assertEqual(expected_role_for_staff, staff_user.role)

    def test_save_transaction(self):
        """
        Test that the `save` method of `CinemaUser` is atomic.
        """
        # Create a new CinemaUser object inside a transaction
        with self.assertRaises(Exception):  # This will trigger a rollback
            with transaction.atomic():
                CinemaUser.objects.create(username='test', password='test_pass', role=UserRole.ADMIN)
                raise Exception("Test exception")  # Simulate an error

        # Check no user with the username 'test' was created due to the rollback.
        self.assertEqual(0, CinemaUser.objects.filter(username='test').count())


class SpectatorProfileModelTestCase(TestCase):
    """
    Test case for the model `:class:SpectatorProfile`.
    """

    def setUp(self):
        # Create a test user
        self.user = CinemaUser.objects.create(
            username='test_user', password='test_pass'
        )

    def test_spectator_profile_creation(self):
        """
        Test the creation of a SpectatorProfile instance.
        """
        expected_spectator_profile = SpectatorProfile.objects.get(user_id=self.user.id)
        self.assertEqual(expected_spectator_profile.user, self.user)
        self.assertEqual(expected_spectator_profile.pk, self.user.pk)
        self.assertEqual(expected_spectator_profile.user.username, self.user.username)
        self.assertEqual(str(expected_spectator_profile), str(self.user))

    def test_get_absolute_url(self):
        """
        Test the correctness of the `get_absolute_url()` method of SpectatorProfile.
        """
        expected_spectator_profile = SpectatorProfile.objects.get(user_id=self.user.id)
        self.assertEqual(
            f"/profile/{expected_spectator_profile.pk}/",
            expected_spectator_profile.get_absolute_url(),
        )
