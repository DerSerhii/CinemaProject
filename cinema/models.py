from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from diploma import settings


class Spectator(AbstractUser):
    wallet = models.DecimalField(default=0,
                                 max_digits=6, decimal_places=2,
                                 verbose_name=_("Top up your account"),
                                 validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = _("Spectator")
        verbose_name_plural = _("Spectator")
        ordering = ["username"]
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"spec_id": self.pk})


class ScreenCinema(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_("Name screen"))
    capacity = models.PositiveSmallIntegerField(verbose_name=_("Capacity"))
    
    class Meta:
        verbose_name = _("Screen")
        verbose_name_plural = _("Screens")
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=130, verbose_name=_("Film"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    starring = models.CharField(max_length=200, verbose_name=_("Starring"))
    director = models.CharField(max_length=50, verbose_name=_("Director"))
    duration = models.DurationField(verbose_name=_("Duration"))
    poster = models.ImageField(null=True, blank=True, upload_to="poster/%Y/%m/%d/",
                               verbose_name=_("Poster"))

    class Meta:
        unique_together = (('name', 'director'),)
        verbose_name = _("Film")
        verbose_name_plural = _("Films")
        ordering = ("name",)
    
    def __str__(self):
        return self.name


class Showtime(models.Model):
    date = models.DateField(verbose_name=_("Showtime date"))
    time_start = models.TimeField(verbose_name=_("Showtime start time"))
    time_end = models.TimeField(verbose_name=_("Showtime end time"))
    screen = models.ForeignKey(ScreenCinema, on_delete=models.PROTECT, verbose_name=_("Screen"))
    film = models.ForeignKey(Film, on_delete=models.PROTECT, verbose_name=_("Film"))
    price = models.DecimalField(default=1, max_digits=5, decimal_places=2,
                                verbose_name=_("Ticket price"),
                                validators=[MinValueValidator(0)])
    attendance = models.PositiveSmallIntegerField(default=0, verbose_name=_("Attendance"))

    class Meta:
        verbose_name = _("Showtime")
        verbose_name_plural = _("Showtimes")
        ordering = ("date",)

    def __str__(self):
        return f"{self.date}-{self.time_start} <{self.film}>"


class Ticket(models.Model):
    spectator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  verbose_name=_("Spectator"))
    showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT,
                                 verbose_name=_("Showtime"),
                                 related_name="tickets")
    quantity = models.PositiveSmallIntegerField(verbose_name=_("Showtime"),
                                                validators=[MinValueValidator(1),
                                                            MaxValueValidator(1000)])
    time_purchase = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ["-time_purchase"]

    def __str__(self):
        return f"Ticket #{self.pk}"
