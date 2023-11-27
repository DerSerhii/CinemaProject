import datetime as dt

from django.core.exceptions import ValidationError
from django.conf import settings

from utils import errors, helpers


class FilmDistributionCreationValidator:

    def __init__(self, cleaned_data: dict):
        self.cleaned_data = cleaned_data
        self.release_day: dt.date = cleaned_data.get('release_day')
        self.last_day: dt.date = cleaned_data.get('last_day')

    def _validate_release_day(self):
        if error := errors.has_showtime_creation_error_in_past(self.release_day):
            raise ValidationError({'release_day': error})

    def _validate_last_day(self):
        if error := errors.has_error_last_day_distribution(self.release_day, self.last_day):
            raise ValidationError({'last_day': error})

    def _validate_start_hour_minute(self):
        start_hour = self.cleaned_data.pop('start_hour')
        start_minute = self.cleaned_data.pop('start_minute')
        start_datetime = helpers.construct_start_datetime(
            self.release_day,
            start_hour,
            start_minute
        )

        if error := errors.has_showtime_creation_error_in_past(start_datetime):
            raise ValidationError({'start_minute': error})

        self.cleaned_data['start_datetime'] = start_datetime

    def _validate_intersection_with_existing_showtimes(self):

        if error := (
                errors.has_error_intersection_with_existing_showtimes(
                    self.cleaned_data.get('screen'),
                    self.cleaned_data.get('film'),
                    self.cleaned_data.get('start_datetime'),
                    self.last_day,
                    settings.TECHNICAL_BREAK_AFTER_SHOWTIME
                )
        ):
            raise ValidationError(error)

    @property
    def data(self):
        """
        Property method to validate and process the data.
        :return: A dictionary containing the validated and processed data.
        :rtype: Dict.
        """
        self._validate_release_day()
        self._validate_last_day()
        self._validate_start_hour_minute()
        self._validate_intersection_with_existing_showtimes()
        return self.cleaned_data
