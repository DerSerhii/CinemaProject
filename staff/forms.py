from django import forms
from django.db.models import Max, Q
from django.utils.translation import gettext as _
from django.utils import timezone as tz
import datetime as dt

from cinema.models import ScreenCinema, Showtime, Film
from diploma import settings


# calculating the end time showtime
def get_time_end_showtime(time_start, duration):
    time_end = (dt.datetime.combine(dt.date(1, 1, 1), time_start)
                + duration
                + settings.TECHNICAL_BREAK_BETWEEN_SESSIONS
                ).time()
    return time_end


def get_overlapping_showtime(time_start, date, date_end, screen):
    max_duration = Film.objects.aggregate(Max("duration"))["duration__max"]
    time_end = get_time_end_showtime(time_start, max_duration)

    if time_start > time_end:
        time_end = dt.time(23, 59)

    q_date = Q(date__range=(date - dt.timedelta(1), date_end))
    q_time_start = Q(time_start__range=(time_start, time_end))
    q_time_end = Q(time_end__range=(time_start, time_end))
    q_screen = Q(screen=screen)
    q_filter = q_date & (q_time_start | q_time_end) & q_screen
    
    return Showtime.objects.filter(q_filter)


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
    date = forms.DateField(widget=forms.SelectDateWidget,
                           initial=tz.localtime(tz.now()).date(),
                           label=_('Showtime date start'))
    date_end = forms.DateField(widget=forms.SelectDateWidget,
                               initial=tz.localtime(tz.now()).date(),
                               label=_('Showtime date end'))

    class Meta:
        model = Showtime
        fields = ("date", "date_end", "time_start", "film", "screen", "price")
    
    def save(self, commit=True):
        form = super().save(commit=False)
        
        period = (self.cleaned_data["date_end"] - form.date).days
        time_end = get_time_end_showtime(form.time_start, form.film.duration)
        
        bulk_list = list()
        for i in range(-1, period):
            bulk_list.append(
                Showtime(
                    date=form.date + dt.timedelta(i + 1),
                    time_start=form.time_start,
                    time_end=time_end,
                    screen=form.screen,
                    film=form.film,
                    price=form.price,
                )
            )
        if commit:
            Showtime.objects.bulk_create(bulk_list)
        
        return form
    
    def clean(self):
        cleaned_data = super().clean()
        screen = cleaned_data["screen"]
        date = cleaned_data["date"]
        date_end = cleaned_data["date_end"]
        time_start = cleaned_data["time_start"]

        if date > date_end:
            raise forms.ValidationError("End date cannot be less than Start date")

        overlapping_showtime = get_overlapping_showtime(time_start, date, date_end, screen)
        if overlapping_showtime:
            raise forms.ValidationError("Showtime overlay")


class ShowtimeEditForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget,
                           label=_("Showtime date"))

    class Meta:
        model = Showtime
        fields = ("date", "time_start", "film", "screen", "price")

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

        overlapping_showtime = get_overlapping_showtime(time_start, date, date, screen)
        if overlapping_showtime.exclude(id=self.showtime_id):
            raise forms.ValidationError("Showtime overlay")

    def save(self, commit=True):
        form = super().save(commit=False)

        form.time_end = get_time_end_showtime(form.time_start, form.film.duration)
        if commit:
            form.save()
        return form
