import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone as tz
from django.utils.translation import gettext as _

from cinema_project import settings


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
    duration: dt.timedelta = models.DurationField(verbose_name=_("Duration"))
    poster = models.ImageField(null=True, blank=True, upload_to="poster/%Y/%m/%d/",
                               verbose_name=_("Poster"))
    to_rental = models.BooleanField(default=True)

    class Meta:
        unique_together = (('name', 'director'),)
        verbose_name = _("Film")
        verbose_name_plural = _("Films")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Showtime(models.Model):
    film: Film = models.ForeignKey(Film, on_delete=models.PROTECT)
    start: tz.datetime = models.DateTimeField(default=tz.localtime)
    end: tz.datetime = models.DateTimeField(default=tz.localtime)
    screen: ScreenCinema = models.ForeignKey(ScreenCinema, on_delete=models.PROTECT)
    price: float = models.DecimalField(default=10, max_digits=5, decimal_places=2,
                                       verbose_name=_("Ticket price"),
                                       validators=[MinValueValidator(0)])
    attendance = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = _("Showtime")
        verbose_name_plural = _("Showtimes")
        ordering = ("start",)

    def __str__(self):
        return f"{tz.localtime(self.start).strftime('%d/%m %H:%M')} <{self.film}> [{self.screen.name}]"

    def clean(self):
        super().clean()
        self._check_start()

        films = self.__class__.objects.filter(screen=self.screen,
                                              start__lte=self.end,
                                              end__gte=self.start)
        # print(self.start)
        # print(self.end)
        # print(films)

    # def save(self, **kwargs):
    #     self.end = self._compute_end_showtime()
    #     super().save(**kwargs)

    def _check_start(self) -> None:
        current_datetime = tz.localtime()
        if self.start < current_datetime:
            err_msg = _("Impossible to create a showtime in the past! "
                        f"Now: {current_datetime.strftime('%d.%m %H:%M')}")
            code = 'check_start_datetime'
            raise ValidationError(err_msg, code=code)

    def _check_film_intersection(self) -> None:
        films = self.__class__.objects.filter(screen=self.screen,
                                              start__lte=self.end,
                                              end__gte=self.start)

    def _compute_end_showtime(self):
        return self.start + self.film.duration + settings.TECHNICAL_BREAK_AFTER_SHOWTIME


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
