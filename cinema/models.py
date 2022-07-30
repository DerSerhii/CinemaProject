from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Spectator(AbstractUser):
    wallet = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Spectator")
        verbose_name_plural = _("Spectator")
        ordering = ["username"]

    def __str__(self):
        return self.username
