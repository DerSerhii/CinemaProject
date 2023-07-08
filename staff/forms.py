import datetime as dt

from typing import Type
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from django.utils.translation import gettext as _
from django.db.models import QuerySet, Q

from cinema.models import ScreenCinema, Showtime
from cinema_project import settings


def get_time_end_showtime(date_start: dt.date,
                          time_start: dt.time,
                          duration: dt.timedelta) -> dt.datetime:
    """
    Return a time_end of a showtime (datatime.datatime), which is calculated based
    on a duration of the showtime, and the technical break between a showtime.
    """
    time_end = (dt.datetime.combine(date_start, time_start, tz.get_current_timezone())
                + duration
                + settings.TECHNICAL_BREAK_BETWEEN_SHOWTIME
                )
    return time_end


def get_overlapping_showtime(data_new_showtime: dict) -> QuerySet:
    """
    Return a QuerySet of overlapping existing showtime with new a showtime.
    """
    screen = data_new_showtime['screen']
    film = data_new_showtime['film']
    date_start = data_new_showtime['date_start']  # obj: datatime.date
    date_end = data_new_showtime['date_end']  # obj: datatime.date
    time_start = data_new_showtime['time_start']  # obj: datatime.time

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
    date_start = data_new_showtime['date_start']  # obj: datatime.date
    date_end = data_new_showtime['date_end']  # obj: datatime.date
    time_start = data_new_showtime['time_start']  # obj: datatime.time

    current_timezone = tz.get_current_timezone()
    datetime_start = dt.datetime.combine(date_start,
                                         time_start,
                                         current_timezone)  # obj: datatime.datetime
    # check Start datetime
    if datetime_start < tz.localtime():
        raise validation_error(
            'ATTENTION: Unable to create a showtime in the past'
        )

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


class ShowtimeForm(forms.ModelForm):
    date_start = forms.DateField(widget=forms.SelectDateWidget,
                                 initial=tz.localtime(tz.now()).date(),
                                 label=_('Showtime date start'))
    date_end = forms.DateField(widget=forms.SelectDateWidget,
                               initial=tz.localtime(tz.now()).date(),
                               label=_('Showtime date end'))
    time_start = forms.TimeField()

    class Meta:
        model = Showtime
        fields = ['date_start', 'date_end', 'time_start', 'film', 'screen', 'price']

    def clean(self):
        cleaned_data = super().clean()
        check_date_time_showtime(cleaned_data, forms.ValidationError)

    def save(self, commit=True):
        form = super().save(commit=False)

        form.date = self.cleaned_data['date_start']

        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        time_start = self.cleaned_data['time_start']

        start = dt.datetime.combine(date_start, time_start)
        end = get_time_end_showtime(date_start, time_start, form.film.duration)
        # Convert Naive datetime.datetime in given timezone Aware
        start_aware = tz.make_aware(start)
        end_aware = tz.make_aware(end)

        period = (date_end - form.date).days

        bulk_list = list()
        for i in range(-1, period):
            bulk_list.append(
                Showtime(
                    start=start_aware + dt.timedelta(i + 1),
                    end=end_aware + dt.timedelta(i + 1),
                    screen=form.screen,
                    film=form.film,
                    price=form.price,
                )
            )
        if commit:
            Showtime.objects.bulk_create(bulk_list)

        return form


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

        form.time_end = get_time_end_showtime(form.time_start, form.film.duration)
        if commit:
            form.save()
        return form

# max_duration = Film.objects.aggregate(Max("duration"))["duration__max"]
