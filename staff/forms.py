import datetime as dt

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from django.utils.translation import gettext as _

import utils
from cinema.models import ScreenCinema, Showtime, Film
from cinema_project import settings


class ScreenField(forms.CharField):
    def to_python(self, value):
        super().to_python(value)
        return value.lower()


class ScreenForm(forms.ModelForm):
    name = ScreenField(max_length=20)

    class Meta:
        model = ScreenCinema
        fields = ("name", "capacity")


class FilmDistributionCreationForm(forms.Form):
    """
    This object represents a form for creating a single showtime
    or film distribution (cycle of showtime) that start at a certain time.
    """
    film = forms.ModelChoiceField(
        queryset=Film.objects.filter(to_rental=True),
        empty_label=_('= select ='),
        widget=forms.Select(attrs={'class': 'form-input-film'}),
        label=_('Film')
    )
    release_day = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-input-date-screen'},
                                      years=utils.derive_range_years()),
        label=_('Release day'),
        initial=tz.localdate()
    )
    last_day = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'form-input-date-screen'},
                                      years=utils.derive_range_years()),
        label=_('Last day'),
        initial=tz.localdate()
    )
    start_hour = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-input-time', 'min': 0, 'max': 23}),
        label=_('Start time'),
        initial=tz.localtime().strftime('%H')
    )
    start_minute = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-input-time', 'min': 0, 'max': 59, 'step': 5}),
        initial=30
    )
    screen = forms.ModelChoiceField(
        queryset=ScreenCinema.objects.all(),
        empty_label=_('= select ='),
        widget=forms.Select(attrs={'class': 'form-input-date-screen'}),
        label=_('Screen')
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-input-time', 'step': 1}),
        label=_('Ticket price'),
        initial=10,
        max_value=1000,
        min_value=0,

    )

    def clean_release_day(self) -> dt.date:
        """
        The `release_day` field undergoes extra cleaning.
        If the release day of film distribution is less than the current day,
        an error will be raised.
        """
        release_day: dt.date = self.cleaned_data.get('release_day')
        if error := utils.has_error_showtime_start(release_day):
            raise ValidationError('👆🏽' + error)
        return release_day

    def clean_last_day(self) -> dt.date:
        """
        The `last_day` field undergoes extra cleaning.
        If the last day of film distribution is less than the current day,
        an error will be raised.
        """
        last_day: dt.date = self.cleaned_data.get('last_day')
        if error := utils.has_error_showtime_start(last_day):
            raise ValidationError('👆🏽' + error)
        return last_day

    def clean(self) -> dict | None:
        """
        Hook for doing extra form-wide cleaning.

        If the last day of distribution film is earlier than the release day,
        then an error will be added to the field `last_day`.

        If the start of showtime is less than the current moment,
        then ah error will be added to the filed `start_minute`.

        If film distribution that is being created has intersections
        with existing showtimes, an error will be raised.
        """
        cleaned_data = super().clean()
        release_day: dt.date = cleaned_data.get('release_day')
        last_day: dt.date = cleaned_data.get('last_day')

        if release_day and last_day:
            if error := utils.has_error_last_day_distribution(release_day, last_day):
                self.add_error('last_day', '👆🏽' + error)
                return

            start_hour = cleaned_data.pop('start_hour')
            start_minute = cleaned_data.pop('start_minute')
            start_datetime = utils.construct_start_datetime(release_day, start_hour, start_minute)

            if error := utils.has_error_showtime_start(start_datetime):
                self.add_error('start_minute', '👆🏽' + error)
                return

            screen = cleaned_data.get('screen')
            film = cleaned_data.get('film')

            if error := (
                utils.has_error_intersection_with_existing_showtimes(
                    screen, film, start_datetime, last_day, settings.TECHNICAL_BREAK_AFTER_SHOWTIME
                )
            ):
                raise ValidationError('📛️\n' + error)

            cleaned_data['start_datetime'] = start_datetime
            return cleaned_data

    def create_film_distribution(self) -> None:
        """
        Method for creating a film distribution (cycle of showtime or single showtime).
        Use if the form is validated.
        """
        film: Film = self.cleaned_data['film']
        release_day: dt.date = self.cleaned_data['release_day']
        last_day: dt.date = self.cleaned_data['last_day']
        start_datetime: dt.datetime = self.cleaned_data['start_datetime']
        screen: ScreenCinema = self.cleaned_data['screen']
        price = self.cleaned_data['price']

        bulk_showtime = []
        for day in range((last_day - release_day).days + 1):
            start = start_datetime + dt.timedelta(days=day)
            end = start + film.duration
            bulk_showtime.append(
                Showtime(film=film, start=start, end=end, screen=screen, price=price)
            )
        Showtime.objects.bulk_create(bulk_showtime)


class ShowtimeEditForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget,
                           label=_("Showtime date"))

    class Meta:
        model = Showtime
        fields = ("date", "start", "film", "screen", "price")

    def __init__(self, showtime_id, attendance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.showtime_id = showtime_id
        self.attendance = attendance

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data["date"]
        time_start = cleaned_data["time_start"]
        screen = cleaned_data["screen"]

        if self.attendance:
            message = f"Editing is no longer available!" \
                      f" {self.attendance} tickets sold per showtime"
            raise forms.ValidationError(message)

        overlapping_showtime = get_overlapping_showtime(cleaned_data)
        if overlapping_showtime.exclude(id=self.showtime_id):
            raise forms.ValidationError("Showtime overlay")

    def save(self, commit=True):
        form = super().save(commit=False)

        form.time_end = get_time_end_showtime(form.start_time, form.film_1_30.duration)
        if commit:
            form.save()
        return form
