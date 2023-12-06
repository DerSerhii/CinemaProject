"""
The module represents test cases for functions of module `validators`.
"""

import datetime as dt

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone as tz

from utils import validators
from cinema_project import constants
from cinema.models import Showtime, Film, ScreenHall


class ShowtimeValidatorTestCase(TestCase):
    """
    Test case for the ShowtimeValidator.
    """

    def setUp(self):
        release_day = tz.localdate() + dt.timedelta(days=1)
        screen_blue = ScreenHall.objects.create(name='blue', slug='blue', capacity=50)
        film_duration = dt.timedelta(hours=1.5)
        film_1_30 = Film.objects.create(
            title='Test Film 1:30 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            release_year=2023,
            duration=film_duration,
        )
        showtime_set = dict(film=film_1_30, screen=screen_blue)
        # Showtime No1
        start_datetime_1 = tz.make_aware(dt.datetime.combine(release_day, dt.time(hour=1)))
        Showtime.objects.create(
            start=start_datetime_1,
            end=start_datetime_1 + film_duration,
            **showtime_set
        )
        # Showtime No2
        start_datetime_2 = tz.make_aware(dt.datetime.combine(release_day, dt.time(hour=3)))
        showtime_2 = Showtime.objects.create(
            start=start_datetime_2,
            end=start_datetime_2 + film_duration,
            **showtime_set
        )

        self.showtime_2 = showtime_2
        self.start_datetime_2 = start_datetime_2
        self.screen_blue = screen_blue

    def test_with_valid_data(self):
        """
        Test ShowtimeValidator with valid data.
        """
        form_cleaned_data = {
            constants.SHOWTIME: self.showtime_2,
            constants.RELEASE_DAY: self.start_datetime_2.date(),
            constants.START_HOUR: self.start_datetime_2.hour + 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        showtime_validator = validators.ShowtimeValidator(form_cleaned_data)
        validated_data = showtime_validator.data
        self.assertEqual(validated_data, form_cleaned_data)

    def test_invalid_release_day(self):
        """
        Test ShowtimeValidator with invalid `release_day`.
        """
        form_cleaned_data = {
            constants.SHOWTIME: self.showtime_2,
            constants.RELEASE_DAY: self.start_datetime_2.date() - dt.timedelta(days=4),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.ShowtimeValidator(form_cleaned_data).data
        self.assertTrue(constants.RELEASE_DAY in context.exception.error_dict)
        self.assertFalse(constants.START_MINUTE in context.exception.error_dict)

    def test_invalid_start_hour_minute(self):
        """
        Test ShowtimeValidator with invalid `start_hour` and `start_minute`.
        """
        form_cleaned_data = {
            constants.SHOWTIME: self.showtime_2,
            constants.RELEASE_DAY: self.start_datetime_2.date() - dt.timedelta(days=1),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.ShowtimeValidator(form_cleaned_data).data
        self.assertFalse(constants.RELEASE_DAY in context.exception.error_dict)
        self.assertTrue(constants.START_MINUTE in context.exception.error_dict)

    def test_intersection_with_existing_showtimes(self):
        """
        Test ShowtimeValidator with intersection_with_existing_showtimes.
        """
        form_cleaned_data = {
            constants.SHOWTIME: self.showtime_2,
            constants.RELEASE_DAY: self.start_datetime_2.date(),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.ShowtimeValidator(form_cleaned_data).data
        self.assertIn('with existing showtimes', context.exception.error_list[0].message)
        self.assertFalse(hasattr(context.exception, 'error_dict'))


class FilmDistributionCreationValidatorTestCase(TestCase):
    """
    Test case for the FilmDistributionCreationValidator.
    """

    def setUp(self):
        release_day = tz.localdate() + dt.timedelta(days=1)
        screen_blue = ScreenHall.objects.create(name='blue', slug='blue', capacity=50)
        film_duration = dt.timedelta(hours=1.5)
        film_1_30 = Film.objects.create(
            title='Test Film 1:30 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            release_year=2023,
            duration=film_duration,
        )
        showtime_set = dict(film=film_1_30, screen=screen_blue)
        # Showtime No1
        start_datetime_1 = tz.make_aware(dt.datetime.combine(release_day, dt.time(hour=1)))
        Showtime.objects.create(
            start=start_datetime_1,
            end=start_datetime_1 + film_duration,
            **showtime_set
        )
        # Showtime No2
        start_datetime_2 = tz.make_aware(dt.datetime.combine(release_day, dt.time(hour=3)))
        showtime_2 = Showtime.objects.create(
            start=start_datetime_2,
            end=start_datetime_2 + film_duration,
            **showtime_set
        )

        self.film = film_1_30
        self.start_datetime_2 = start_datetime_2
        self.screen_blue = screen_blue

    def test_with_valid_data(self):
        """
        Test FilmDistributionCreationValidator with valid data.
        """
        form_cleaned_data = {
            constants.FILM: self.film,
            constants.RELEASE_DAY: self.start_datetime_2.date(),
            constants.LAST_DAY: self.start_datetime_2.date(),
            constants.START_HOUR: self.start_datetime_2.hour + 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        showtime_validator = validators.FilmDistributionCreationValidator(form_cleaned_data)
        validated_data = showtime_validator.data
        self.assertEqual(validated_data, form_cleaned_data)

    def test_invalid_release_day(self):
        """
        Test FilmDistributionCreationValidator with invalid `release_day`.
        """
        form_cleaned_data = {
            constants.FILM: self.film,
            constants.RELEASE_DAY: self.start_datetime_2.date() - dt.timedelta(days=4),
            constants.LAST_DAY: self.start_datetime_2.date() - dt.timedelta(days=4),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.FilmDistributionCreationValidator(form_cleaned_data).data
        self.assertTrue(constants.RELEASE_DAY in context.exception.error_dict)
        self.assertFalse(constants.LAST_DAY in context.exception.error_dict)
        self.assertFalse(constants.START_MINUTE in context.exception.error_dict)

    def test_invalid_last_day(self):
        """
        Test FilmDistributionCreationValidator with invalid `last_day`.
        """
        form_cleaned_data = {
            constants.FILM: self.film,
            constants.RELEASE_DAY: self.start_datetime_2.date() - dt.timedelta(days=1),
            constants.LAST_DAY: self.start_datetime_2.date() - dt.timedelta(days=4),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.FilmDistributionCreationValidator(form_cleaned_data).data
        self.assertFalse(constants.RELEASE_DAY in context.exception.error_dict)
        self.assertTrue(constants.LAST_DAY in context.exception.error_dict)
        self.assertFalse(constants.START_MINUTE in context.exception.error_dict)

    def test_invalid_start_hour_minute(self):
        """
        Test FilmDistributionCreationValidator with invalid `start_hour` and `start_minute`.
        """
        form_cleaned_data = {
            constants.FILM: self.film,
            constants.RELEASE_DAY: self.start_datetime_2.date() - dt.timedelta(days=1),
            constants.LAST_DAY: self.start_datetime_2.date(),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.FilmDistributionCreationValidator(form_cleaned_data).data
        self.assertFalse(constants.RELEASE_DAY in context.exception.error_dict)
        self.assertFalse(constants.LAST_DAY in context.exception.error_dict)
        self.assertTrue(constants.START_MINUTE in context.exception.error_dict)

    def test_intersection_with_existing_showtimes(self):
        """
        Test FilmDistributionCreationValidator with intersection_with_existing_showtimes.
        """
        form_cleaned_data = {
            constants.FILM: self.film,
            constants.RELEASE_DAY: self.start_datetime_2.date(),
            constants.LAST_DAY: self.start_datetime_2.date(),
            constants.START_HOUR: self.start_datetime_2.hour - 2,
            constants.START_MINUTE: 0,
            constants.SCREEN: self.screen_blue
        }
        with self.assertRaises(ValidationError) as context:
            data = validators.FilmDistributionCreationValidator(form_cleaned_data).data
        self.assertIn('with existing showtimes', context.exception.error_list[0].message)
        self.assertFalse(hasattr(context.exception, 'error_dict'))
