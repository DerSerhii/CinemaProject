"""
The module represents test cases for forms of module `forms`.
"""

import datetime as dt

from django.test import TestCase
from django.utils import timezone as tz
from django.utils.translation import gettext as _

from cinema.models import ScreenCinema, Film, Showtime
from staff.forms import FilmDistributionCreationForm


class FilmDistributionCreationFormTestCase(TestCase):
    """
    Test case for the form `:class:FilmDistributionCreationForm`.
    """

    def setUp(self):
        self.maxDiff = None

        self.screen_blue = ScreenCinema.objects.create(name='blue', capacity=50)
        self.film_1_30 = Film.objects.create(
            name='Test Film 1:30 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            duration=dt.timedelta(hours=1.5)
        )
        self.start = (tz.localtime() + dt.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        self.yesterday = self.start.date() - dt.timedelta(days=1)

    def test_form_valid_with_creating_single_showtime(self):
        """
        Single showtime creation test.
        Also, checking fields of the `Showtime` object according to the data being filled in.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': self.start.date(),
            'last_day': self.start.date(),
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': 15.00,
        }
        # Form valid test
        form = FilmDistributionCreationForm(form_data)
        self.assertTrue(form.is_valid())

        # Quantity of showtime test
        form.create_film_distribution()
        showtimes = Showtime.objects.filter(film=self.film_1_30, screen=self.screen_blue)
        self.assertEqual(1, showtimes.count())

        # Showtime fields validation test
        showtime = showtimes.first()
        start_from_showtime = showtime.start
        last_day_from_showtime = showtime.end.date()
        film_name_from_showtime = showtime.film.name
        screen_name_from_showtime = showtime.screen.name
        price_from_showtime = showtime.price
        self.assertEqual(self.start, start_from_showtime)
        self.assertEqual(self.start.date(), last_day_from_showtime)
        self.assertEqual('Test Film 1:30 hour', film_name_from_showtime )
        self.assertEqual('blue', screen_name_from_showtime)
        self.assertEqual(15.00, price_from_showtime)

    def test_form_valid_with_creating_ten_showtime(self):
        """
        Film distribution creation test consisting with ten showtimes.
        Also, checking the start of the last day.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': self.start.date(),
            'last_day': self.start.date() + dt.timedelta(days=9),
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': 15.00,
        }
        # Form valid test
        form = FilmDistributionCreationForm(form_data)
        self.assertTrue(form.is_valid())

        # Quantity of showtime test
        form.create_film_distribution()
        showtimes = Showtime.objects.filter(film=self.film_1_30, screen=self.screen_blue)
        self.assertEqual(10, showtimes.count())

        # Checking the start of the last day
        showtime = showtimes.last()
        expected_start_last_day = self.start + dt.timedelta(days=9)
        start_last_day_from_showtime = showtime.start
        self.assertEqual(expected_start_last_day, start_last_day_from_showtime)

    def test_invalid_form_passed_day_less_than_current_day(self):
        """
        Testing extra cleaning for fields `release_day` and `last_day`.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': self.yesterday,
            'last_day': self.yesterday,
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': 15.00,
        }
        form = FilmDistributionCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_day', form.errors)
        self.assertIn('last_day', form.errors)
        error_message = _('Impossible to create a showtime in the past!')
        self.assertIn(error_message, ''.join(form.errors['release_day']))
        self.assertIn(error_message, ''.join(form.errors['last_day']))

    def test_invalid_form_last_day_less_than_release_day(self):
        """
        Testing `clean` hook for the occasion:
        last day of distribution film is earlier than the release day.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': self.start.date(),
            'last_day': self.yesterday,
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': 15.00,
        }
        form = FilmDistributionCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertNotIn('release_day', form.errors)
        self.assertIn('last_day', form.errors)
        error_message = _('Impossible to create a showtime in the past!')
        self.assertIn(error_message, ''.join(form.errors['last_day']))

    def test_invalid_form_start_less_than_current_moment(self):
        """
        Testing `clean` hook for the occasion:
        the start of showtime is less than the current moment.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': tz.localdate(),
            'last_day': tz.localdate(),
            'start_hour': tz.localtime().hour,
            'start_minute': tz.localtime().minute,
            # before calling the form validation, the time will increase
            'screen': self.screen_blue,
            'price': 15.00,
        }
        form = FilmDistributionCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_minute', form.errors)
        error_message = _('Impossible to create a showtime in the past!')
        self.assertIn(error_message, ''.join(form.errors['start_minute']))


    def test_invalid_form_has_intersection_with_existing_showtimes(self):
        """
        Testing `clean` hook for the occasion:
        the film distribution that is being created has intersections
        with existing showtimes.
        """
        Showtime.objects.create(
            film=self.film_1_30,
            start=self.start,
            end=self.start + self.film_1_30.duration,
            screen=self.screen_blue
        )
        form_data = {
            'film': self.film_1_30,
            'release_day': self.start.date(),
            'last_day': self.start.date(),
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': 15.00,
        }
        form = FilmDistributionCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        error_message = _('intersection(s) with existing showtimes')
        self.assertIn(error_message, ''.join(form.errors['__all__']))

    def test_invalid_form_price_negative_number(self):
        """
        Testing the `price` field for the case when a negative number is passed.
        """
        form_data = {
            'film': self.film_1_30,
            'release_day': self.start.date(),
            'last_day': self.start.date(),
            'start_hour': self.start.hour,
            'start_minute': self.start.minute,
            'screen': self.screen_blue,
            'price': -15.00,
        }
        form = FilmDistributionCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
