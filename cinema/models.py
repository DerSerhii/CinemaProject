"""
The module represents models for application `cinema`.

This module contains model definitions for the cinema system, including
, cinema halls, films, showtimes and tickets.
"""

import datetime as dt

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone as tz
from django.utils.translation import gettext as _


class ScreenHall(models.Model):
    name = models.CharField(_('hall name'), max_length=20, unique=True)
    slug = models.SlugField(_('slug'), max_length=20, unique=True)
    capacity = models.PositiveSmallIntegerField(_('capacity'))

    class Meta:
        db_table = 'screen_halls'
        verbose_name = _('screen hall')
        verbose_name_plural = _('screen halls')
        ordering = ['name']

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(_('film title'), max_length=150)
    duration: dt.timedelta = models.DurationField(_('duration'))
    is_active = models.BooleanField(_('active'), default=True)
    release_year = models.PositiveSmallIntegerField(_('release day'))
    description = models.TextField(_('description'), blank=True)
    starring = models.CharField(_('starring'), max_length=255)
    director = models.CharField(_('director'), max_length=50)
    poster = models.ImageField(_('poster'), upload_to='poster/%Y/%m/%d/', null=True)

    class Meta:
        db_table = 'films'
        unique_together = [('title', 'director')]
        verbose_name = _('film')
        verbose_name_plural = _('films')
        ordering = ['release_year', 'title']

    def __str__(self):
        return self.title


class Showtime(models.Model):
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    start = models.DateTimeField(_('the film start'))
    end = models.DateTimeField(_('the film end'))
    screen = models.ForeignKey(ScreenHall, on_delete=models.PROTECT)
    price = models.DecimalField(
        _('ticket price'),
        max_digits=5, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    attendance = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'showtimes'
        verbose_name = _('showtime')
        verbose_name_plural = _('showtimes')
        ordering = ('start',)

    def __str__(self):
        return f"{tz.localtime(self.start).strftime('%d/%m %H:%M')} <{self.film}> [{self.screen.name}]"


class Ticket(models.Model):
    spectator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT, related_name="tickets")
    quantity = models.PositiveSmallIntegerField(
        _('quantity'),
        validators=[MinValueValidator(1),
                    MaxValueValidator(100)]
    )
    purchase_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tickets'
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
        ordering = ['-purchase_time']

    def __str__(self):
        return f"Ticket #{self.pk}"
