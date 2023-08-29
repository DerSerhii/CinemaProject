"""
The module represents models for application `cinema_admin`.

This module contains the definition of the cinema user model
within the Django authentication system.
Also, related with this model is a spectator profile model.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext as _


class UserRole(models.TextChoices):
    """
    Enum-like class that defines user roles in the cinema system.
    """
    ADMIN = 'AD', _('Administrator')
    SPECTATOR = 'SP', _('Spectator')


class CinemaUser(AbstractUser):
    """
    Extended user model for the cinema system.
    This model allows users to have different roles in the cinema system:
    `Administrator` and `Spectator`.

    Users within the Django authentication system are represented by this model.
    Username, password and role are required.
    By default, role is 'Spectator'.
    Other fields are optional.

    Site superusers and staffs automatically get `Administrator` role.

    Users with `Spectator` role automatically get Spectator Profile
    with advanced attributes.
    """

    role = models.CharField(
        _('cinema system role'),
        max_length=2,
        default=UserRole.SPECTATOR,
        choices=UserRole.choices
    )

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('all users')
        ordering = ['username']

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Overridden default save method to set the role to `Administrator`
        for superusers and staffs of the site.
        Also, automatically creating Spectator Profile for `Spectator` role.
        """
        # Superusers and staffs can't be spectators
        if self.is_superuser or self.is_staff:
            self.role = UserRole.ADMIN

        super().save(*args, **kwargs)

        # If a user with the `spectator` role has just been created,
        # Spectator Profile will be automatically created.
        if self.role == UserRole.SPECTATOR and not hasattr(self, 'profile'):
            SpectatorProfile.objects.create(user=self)

    def is_admin(self):
        """
        Check whether the cinema user has the `Administrator` role.
        """
        return self.role == UserRole.ADMIN


class SpectatorProfile(models.Model):
    """
    Model represents a profile of a spectator.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    account = models.DecimalField(
        _('account'),
        max_digits=6, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = 'spectator_profiles'
        verbose_name = _('spectator profile')
        verbose_name_plural = _('spectator profiles')
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'spec_id': self.pk})

