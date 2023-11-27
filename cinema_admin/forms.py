import datetime as dt

from django import forms
from django.utils import timezone as tz
from django.utils.translation import gettext as _

import utils
from cinema.models import ScreenHall, Showtime, Film
from cinema_admin.models import CinemaUser, UserRole


class AdminCinemaUserForm(forms.ModelForm):
    """
    A custom form for creating administrator users in the cinema system.
    This form extends the built-in ModelForm and customizes the saving process
    to set the user role as 'Administrator' and hash the password.
    """

    class Meta:
        model = CinemaUser
        exclude = ['role']

    def save(self, commit=True):
        """
        Overridden method to set the user role, hash the password, and save the user.

        Only administrators with different rights can be created from the administrative panel.
        Spectators must be created by the spectators themselves during registration.
        """
        user = super().save(commit=False)
        user.role = UserRole.ADMIN
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class FilmDistributionCreationForm(forms.Form):
    """
    This object represents a form for creating a film distribution
    (single showtime or cycle of showtime that start at a certain time).
    """
    film = forms.ModelChoiceField(
        queryset=Film.objects.filter(is_active=True),
        empty_label=_('= select ='),
        widget=forms.Select(attrs={'class': 'form-input-film'}),
        label=_('Film')
    )
    release_day = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-input-date-screen'},
            years=utils.derive_range_years()
        ),
        label=_('Release day'),
        initial=tz.localdate()
    )
    last_day = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-input-date-screen'},
            years=utils.derive_range_years()
        ),
        label=_('Last day'),
        initial=tz.localdate()
    )
    start_hour = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input-time',
                'min': 0,
                'max': 23
            }
        ),
        label=_('Start time'),
        initial=tz.localtime().strftime('%H')
    )
    start_minute = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input-time',
                'min': 0,
                'max': 59,
                'step': 5
            }
        ),
        initial=30
    )
    screen = forms.ModelChoiceField(
        queryset=ScreenHall.objects.all(),
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

    def clean(self) -> dict | None:
        """
        Hook for doing extra form-wide cleaning.

        If the release day of film distribution is less than today,
        then an error will be raised to the field `release_day`.

        If the last day of film distribution is earlier than the release day,
        then an error will be raised to the field `last_day`.

        If the start time of showtime is less than the current moment,
        then ah error will be raised to the filed `start_minute`.

        If film distribution that is being created has intersections
        with existing showtimes, an error will be raised.
        """
        cleaned_data: dict = super().clean()
        validator = utils.FilmDistributionCreationValidator(cleaned_data)
        return validator.data

    def create_film_distribution(self) -> None:
        """
        Method for creating a film distribution (cycle of showtime or single showtime).
        Use if the form is validated.
        """
        film: Film = self.cleaned_data['film']
        release_day: dt.date = self.cleaned_data['release_day']
        last_day: dt.date = self.cleaned_data['last_day']
        start_datetime: dt.datetime = self.cleaned_data['start_datetime']
        screen: ScreenHall = self.cleaned_data['screen']
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

class ScreenField(forms.CharField):
    def to_python(self, value):
        super().to_python(value)
        return value.lower()


class ScreenForm(forms.ModelForm):
    name = ScreenField(max_length=20)

    class Meta:
        model = ScreenHall
        fields = ("name", "capacity")