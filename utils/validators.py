"""
The module represents VALIDATORS for use in FORMS and SERIALIZERS of the project.
"""

import datetime as dt

from django.core.exceptions import ValidationError
from django.conf import settings

from utils import errors, helpers
from cinema_project import constants


class ShowtimeValidator:
    """
    Validator for creating and editing Showtime (single showtime only).
    """
    release_day_key = constants.RELEASE_DAY
    start_hour_key = constants.START_HOUR
    start_minute_key = constants.START_MINUTE
    start_datetime_key = constants.START_DATETIME

    def __init__(self, cleaned_data: dict):
        self.cleaned_data = cleaned_data
        self.release_day: dt.date = cleaned_data.get(self.release_day_key)

    def _validate_release_day(self):
        """
        Validates the `release_day` and raises a ValidationError if it's in the past.
        """
        if error := errors.has_showtime_creation_error_in_past(self.release_day):
            raise ValidationError({self.release_day_key: error})

    def _validate_start_hour_minute(self):
        """
        Validates `start_hour` and `start_minute`, and constructs the start datetime.
        Raises a ValidationError if start time is in the past.
        Adds validated `start_datatime` to cleaned data.
        """
        start_hour = self.cleaned_data.pop(self.start_hour_key)
        start_minute = self.cleaned_data.pop(self.start_minute_key)
        start_datetime = helpers.construct_start_datetime(
            self.release_day,
            start_hour,
            start_minute
        )

        if error := errors.has_showtime_creation_error_in_past(start_datetime):
            raise ValidationError({self.start_minute_key: error})

        self.cleaned_data[self.start_datetime_key] = start_datetime

    def _validate_intersection_with_existing_showtimes(self):
        """
        Validates if there are intersections with existing showtimes
        and raises a ValidationError if found.
        """
        if error := (
                errors.has_error_intersection_with_existing_showtimes(
                    self.cleaned_data,
                    settings.TECHNICAL_BREAK_AFTER_SHOWTIME,
                )
        ):
            raise ValidationError(error)

    @property
    def data(self):
        """
        Property method to validate and process the data.
        :return: A dictionary containing the validated and processed data.
        :rtype: Dict.

        Attention!
        The position of the validators is important for the form.
        """
        self._validate_release_day()
        self._validate_start_hour_minute()
        self._validate_intersection_with_existing_showtimes()

        return self.cleaned_data


class FilmDistributionCreationValidator(ShowtimeValidator):
    """
    Validator for creating film distribution (bulk showtime creation),
    extends ShowtimeValidator.
    """
    last_day_key = constants.LAST_DAY

    def _validate_last_day(self):
        """
        Validates `last_day` of the film distribution.
        Raises a ValidationError if there's an error.
        """
        last_day: dt.date = self.cleaned_data.get(self.last_day_key)
        if error := errors.has_error_last_day_distribution(self.release_day, last_day):
            raise ValidationError({self.last_day_key: error})

    @property
    def data(self):
        """
        Property method to validate and process the data.
        :return: A dictionary containing the validated and processed data.
        :rtype: Dict.

        Attention!
        The position of the validators is important for the form.
        """
        self._validate_release_day()
        self._validate_last_day()
        self._validate_start_hour_minute()
        self._validate_intersection_with_existing_showtimes()

        return self.cleaned_data
