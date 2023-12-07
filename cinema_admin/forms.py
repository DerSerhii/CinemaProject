import datetime as dt

from django import forms
from django.utils import timezone as tz
from django.utils.translation import gettext as _

import utils
from cinema_project import constants
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


class ShowtimeFormMixin(forms.Form):
    """
    A mixin for creating a form related to Showtime model.

    This mixin includes form fields:
        — `release_day` (forms.DateField): A field for selecting the release day.
        — `start_hour` (forms.IntegerField): A field for entering the start hour.
        — `start_minute` (forms.IntegerField): A field for entering the start minute.
        — `screen` (forms.ModelChoiceField): A field for selecting the screen.
        — `price` (forms.DecimalField): A field for entering the ticket price.
    It provides default values and widgets for these fields.
    """

    release_day = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-input-date-screen'},
            years=utils.derive_range_years()
        ),
        label=_('Release day'),
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


class FilmDistributionCreationForm(ShowtimeFormMixin, forms.Form):
    """
    Form class for creating a film distribution
    (single showtime or cycle of showtime that start at a certain time).
    Creates `Showtime` instances.
    """
    film = forms.ModelChoiceField(
        queryset=Film.objects.filter(is_active=True),
        empty_label=_('= select ='),
        widget=forms.Select(attrs={'class': 'form-input-film'}),
        label=_('Film')
    )
    last_day = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={'class': 'form-input-date-screen'},
            years=utils.derive_range_years()
        ),
        label=_('Last day'),
        initial=tz.localdate()
    )

    field_order = (
        'film',
        'release_day',
        'last_day',
        'start_hour',
        'start_minute',
        'screen',
        'price'
    )

    def clean(self) -> dict | None:
        """
        Hook for doing extra form-wide cleaning.
        Validates the form data and return the cleaned data.

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
        film: Film = self.cleaned_data.get(constants.FILM)
        release_day: dt.date = self.cleaned_data.get(constants.RELEASE_DAY)
        last_day: dt.date = self.cleaned_data.get(constants.LAST_DAY)
        start_datetime: dt.datetime = self.cleaned_data.get(constants.START_DATETIME)
        screen: ScreenHall = self.cleaned_data.get(constants.SCREEN)
        price = self.cleaned_data.get(constants.PRICE)

        bulk_showtime = []
        for day in range((last_day - release_day).days + 1):
            start = start_datetime + dt.timedelta(days=day)
            end = start + film.duration
            bulk_showtime.append(
                Showtime(film=film, start=start, end=end, screen=screen, price=price)
            )
        Showtime.objects.bulk_create(bulk_showtime)


class ShowtimeEditForm(ShowtimeFormMixin, forms.ModelForm):
    """
    Form class for editing `Showtime` instances.
    """

    class Meta:
        model = Showtime
        fields = ('release_day', 'start_hour', 'start_minute', 'screen', 'price')

    def clean(self):
        """
        Validates the form data and return the cleaned data.

        This method performs additional validation using the `ShowtimeValidator`
        and updates the cleaned data with the `constants.SHOWTIME` key pointing to
        the instance.

        If the release day of showtime is less than today,
        then an error will be raised to the field `release_day`.

        If the last day of showtime is earlier than the release day,
        then an error will be raised to the field `last_day`.

        If the start time of showtime is less than the current moment,
        then ah error will be raised to the filed `start_minute`.

        If showtime that is being created has intersections
        with existing showtimes, an error will be raised.
        """
        cleaned_data: dict = super().clean()
        cleaned_data.update(
            {constants.SHOWTIME: self.instance}
        )
        validator = utils.ShowtimeValidator(cleaned_data)
        return validator.data

    def save(self, commit=True):
        """
        Saves `Showtime` instance to the database.

        This method overrides the default `save` behavior to set the `start` and `end`
        attributes of the `Showtime` instance based on the cleaned data.

        :returns: The saved `Showtime` instance.
        """
        showtime = super().save(commit=False)

        start_datetime: dt.datetime = self.cleaned_data.get(constants.START_DATETIME)
        showtime.start = start_datetime
        showtime.end = start_datetime + showtime.film.duration

        if commit:
            showtime.save()

        return showtime


class ScreenField(forms.CharField):
    def to_python(self, value):
        super().to_python(value)
        return value.lower()


class ScreenForm(forms.ModelForm):
    name = ScreenField(max_length=20)

    class Meta:
        model = ScreenHall
        fields = ('name', 'capacity')
