import datetime as dt
from typing import Type


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from django.utils.translation import gettext as _
from django.db.models import QuerySet, Q
from django.db import connection

import utils
from cinema.models import ScreenCinema, Showtime, Film
from cinema_project import settings


def get_overlapping_showtime(data_new_showtime: dict) -> QuerySet:
    """
    Return a QuerySet of overlapping existing showtime with new a showtime.
    """
    screen = data_new_showtime['screen']
    film = data_new_showtime['film']
    date_start = data_new_showtime['start_date']  # obj: datatime.date
    date_end = data_new_showtime['end_date']  # obj: datatime.date
    time_start = data_new_showtime['start_time']  # obj: datatime.time

    datetime_start = dt.datetime.combine(date_start,
                                         time_start,
                                         tz.get_current_timezone())  # obj: datatime.datetime
    datetime_end = get_time_end_showtime(date_end,
                                         time_start,
                                         film.duration)  # obj: datatime.datetime
    time_end = datetime_end.time()  # obj: datatime.time

    dt_range = (datetime_start, datetime_end)
    cross_showtime = Showtime.objects.filter(Q(start__range=dt_range)
                                             | Q(end__range=dt_range),
                                             screen=screen
                                             )
    # filter settings
    if time_start < time_end:
        filter_time_start = Q(start__time__range=(time_start, time_end))
        filter_time_end = Q(end__time__range=(time_start, time_end))
    else:
        filter_time_start_to_midnight = Q(start__time__range=(time_start, dt.time.max))
        filter_time_start_past_midnight = Q(start__time__range=(dt.time.min, time_end))
        filter_time_start = filter_time_start_to_midnight | filter_time_start_past_midnight
        filter_time_end = Q(end__time__range=(dt.time.min, time_end))

    return cross_showtime.filter(filter_time_start | filter_time_end)


def check_date_time_showtime(data_new_showtime: dict,
                             validation_error: Type[ValidationError]):
    """

    """
    date_start = data_new_showtime['start_date']  # obj: datatime.date
    date_end = data_new_showtime['start_date']  # obj: datatime.date
    time_start = data_new_showtime['start_time']  # obj: datatime.time

    current_timezone = tz.get_current_timezone()
    datetime_start = dt.datetime.combine(date_start,
                                         time_start,
                                         current_timezone)  # obj: datatime.datetime
    # check Start datetime
    if datetime_start < tz.localtime():
        raise validation_error('ATTENTION: Unable to create a showtime in the past' )

    # check End date
    if date_start > date_end:
        raise validation_error(
            "ATTENTION: END DATE can't be earlier than START DATE"
        )

    cross_showtime = get_overlapping_showtime(data_new_showtime)
    if cross_showtime:
        raise validation_error(
            f'ATTENTION: Showtime overlap with {cross_showtime.count()} sessions. '
            f'Nearest: {cross_showtime.first()}'
        )


class ScreenField(forms.CharField):
    def to_python(self, value):
        super().to_python(value)
        return value.lower()


class ScreenForm(forms.ModelForm):
    name = ScreenField(max_length=20)

    class Meta:
        model = ScreenCinema
        fields = ("name", "capacity")


class FilmRentalCreationForm(forms.Form):
    """
    This object represents a form for creating a single showtime or cycle of showtime
    that start at a certain time.
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

    def clean_release_day(self) -> tz.datetime.date:
        release_day: dt.date = self.cleaned_data.get('release_day')
        if error := utils.has_error_showtime_start(release_day):
            raise ValidationError('👆🏽' + error)
        return release_day

    def clean_last_day(self) -> tz.datetime.date:
        last_day: dt.date = self.cleaned_data.get('last_day')
        if error := utils.has_error_showtime_start(last_day):
            raise ValidationError('👆🏽' + error)
        return last_day

    def clean(self) -> dict | None:
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
                utils.has_error_intersection_with_existing_showtime(
                    screen, film, start_datetime, last_day
                )
            ):
                raise ValidationError(error)

            cleaned_data['start_datetime'] = start_datetime
            return cleaned_data

    def create_film_distribution(self) -> None:
        film: Film = self.cleaned_data['film']
        release_day: dt.date = self.cleaned_data['release_day']
        last_day: dt.date = self.cleaned_data['last_day']
        start_datetime = self.cleaned_data['start_datetime']
        screen = self.cleaned_data['screen']
        price = self.cleaned_data['price']

        bulk_showtime = []
        for day in range((last_day - release_day).days + 1):
            start = start_datetime + dt.timedelta(days=day)
            bulk_showtime.append(
                Showtime(
                    film=film,
                    start=start,
                    end=(start + film.duration),
                    screen=screen,
                    price=price,
                )
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
