"""
The module represents test cases for functions of module `errors`.
"""

import datetime as dt

from django.test import TestCase
from django.utils import timezone as tz
from django.utils.translation import gettext as _

from utils import errors, helpers
from cinema_project import constants
from cinema.models import ScreenHall, Film, Showtime


class HasErrorShowtimeStartTestCase(TestCase):
    """
    Test case for the `has_error_showtime_start` function.
    """

    def setUp(self):
        self.now = tz.localtime()
        self.error_message = 'Impossible to create a showtime in the past! %s'

    def test_past_date(self):
        current_date = self.now.date()
        past_date = current_date - dt.timedelta(days=1)
        now_msg = f"Today is {current_date.strftime('%-d %b, %Y')}"
        error_message =  self.error_message % now_msg
        result = utils.has_error_showtime_start(past_date)
        self.assertEqual(error_message, result)

    def test_current_date(self):
        current_date = self.now.date()
        result = utils.has_error_showtime_start(current_date)
        self.assertEqual(None, result)

    def test_past_datetime(self):
        current_datetime = self.now
        past_datetime = current_datetime - dt.timedelta(minutes=1)
        now_msg = f"Now: {current_datetime.strftime('%-d %b %H:%M')}"
        error_message = self.error_message % now_msg
        result = utils.has_error_showtime_start(past_datetime)
        self.assertEqual(error_message, result)

    def test_future_datetime(self):
        current_datetime = self.now
        future_datetime = current_datetime + dt.timedelta(minutes=1)
        result = utils.has_error_showtime_start(future_datetime)
        self.assertEqual(None, result)

    def test_invalid_input_type(self):
        invalid_input = str(self.now)
        with self.assertRaises(ValueError):
            utils.has_error_showtime_start(invalid_input)


class HasErrorLastDayDistributionTestCase(TestCase):
    """
    Test case for the `has_error_last_day_distribution` function.
    """

    def setUp(self):
        self.start_day = dt.date(2023, 8, 3)
        self.error_message = "The last day of film distribution can't be earlier than the beginning"

    def test_last_day_earlier_than_start(self):
        last_day = dt.date(2023, 8, 2)
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(self.error_message, result)

    def test_last_day_same_as_start(self):
        last_day = self.start_day
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(None, result)

    def test_last_day_later_than_start(self):
        last_day = dt.date(2023, 8, 4)
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(None, result)


class HasErrorIntersectionWithExistingShowtimesTestCase(TestCase):
    """
    Test case for the `has_error_intersection_with_existing_showtimes` function.
    """

    def setUp(self):
        self.maxDiff = None

        # **************************** Screen Set ******************************
        self.screen_blue = ScreenHall.objects.create(name='blue', slug='blue', capacity=50)
        self.screen_green = ScreenHall.objects.create(name='green', slug='green', capacity=50)

        # ****************************** Film Set ******************************
        film_duration = dt.timedelta(hours=1.5)
        # Film_No.1 [1:30]
        self.film_1_30 = Film.objects.create(
            title='Test Film 1:30 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            release_year=2023,
            duration=film_duration
        )
        # Film_No.1 [2:00]
        self.film_2_00 = Film.objects.create(
            title='Test Film 2:00 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            release_year=2023,
            duration=film_duration + dt.timedelta(minutes=30)
        )

        # ****************************** Showtime Set ******************************
        start_datetime_sw1 = dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00')
        bulk_showtime = []
        for day in range(10):
            start = start_datetime_sw1 + dt.timedelta(days=day)
            end = start + self.film_1_30.duration
            bulk_showtime.append(
                Showtime(film=self.film_1_30, start=start, end=end, screen=self.screen_blue)
            )
        Showtime.objects.bulk_create(bulk_showtime)

        start_datetime_sw0 = dt.datetime.fromisoformat('2022-12-31 01:00:00+02:00')
        Showtime.objects.create(
            film=self.film_2_00,
            start=start_datetime_sw0,
            end=start_datetime_sw0 + self.film_2_00.duration,
            screen=self.screen_blue
        )

        # *************************** Technical Break Set ******************************
        self.technical_break_after_showtime_30 = helpers.get_technical_break_after_showtime(
            dt.timedelta(minutes=30)
        )
        self.technical_break_after_showtime_1 = helpers.get_technical_break_after_showtime(
            dt.timedelta(minutes=1)
        )
        self.technical_break_after_showtime_0 = helpers.get_technical_break_after_showtime(
            dt.timedelta(minutes=0)
        )

    def test_no_intersections(self):
        """
        A new showtime doesn't intersect with an existing one.
        [1:00-3:00*) – existing Showtime No.1
        [3:00-5:00*) << new test showtime being created
        * – with technical break after a showtime.
        Should return `None`.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 03:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertIsNone(result)

    def test_has_one_intersection(self):
        """
        A new showtime intersects with an existing one once.
        [1:00-3:00*) – existing Showtime No.1
        [2:00-4:00*) << new test showtime being created
        * – with technical break after a showtime.
        Should return an error message.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_message = _('The film distribution that is being created '
                             'has 1 intersection(s) with existing showtimes:\n'
                             '1) 1 Jan 1:00–2:59* "Test Film 1:30 hour".\n'
                             ' * Attention! Intersections take into account '
                             'the technical break (30 min) after a showtime.')
        self.assertEqual(expected_message, result)

    def test_has_five_intersections(self):
        """
        New showtimes intersect with existing ones five times.
        [01/01 1:00-3:00*) – existing Showtime No.1
        [01/01 2:00-4:00*) << new test showtime No.1t being created
        …
        [05/01 1:00-3:00*) – existing Showtime No.5
        [05/01 2:00-4:00*) << new test showtime No.5t being created
        Should return an error message.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-05'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_message = _('The film distribution that is being created '
                             'has 5 intersection(s) with existing showtimes:\n'
                             '1) 1 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '2) 2 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '3) 3 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '4) 4 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '5) 5 Jan 1:00–2:59* "Test Film 1:30 hour".\n'
                             ' * Attention! Intersections take into account '
                             'the technical break (30 min) after a showtime.')
        self.assertEqual(expected_message, result)

    def test_has_ten_intersections(self):
        """
        New showtimes intersect with existing ones ten times.
        [01/01 1:00-3:00*) – existing Showtime No.1
        [01/01 2:00-4:00*) << new test showtime No.1t being created
        …
        [10/01 1:00-3:00*) – existing Showtime No.10
        [10/01 2:00-4:00*) << new test showtime No.10t being created
        Should return an error message.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-10'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_message = _('The film distribution that is being created '
                             'has 10 intersection(s) with existing showtimes:\n'
                             '1) 1 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '2) 2 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '3) 3 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '4) 4 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '5) 5 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '... and other 5 intersection(s).\n'
                             ' * Attention! Intersections take into account '
                             'the technical break (30 min) after a showtime.')
        self.assertEqual(expected_message, result)

    def test_has_six_intersections_and_one_other_film(self):
        """
        New showtimes intersect with existing ones six times.
        [31/12/2022 1:00-3:00*) – existing Showtime No.0
        [01/01/2023 2:00-4:30*) << new test showtime No.0t being created
        [01/01/2023 1:00-3:00*) – existing Showtime No.1
        [01/01/2023 2:00-4:00*) << new test showtime No.1t being created
        …
        [10/01/2023 1:00-3:00*) – existing Showtime No.10
        [10/01/2023 2:00-4:00*) << new test showtime No.10t being created
        Should return an error message.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2022-12-31 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-05'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_message = _('The film distribution that is being created '
                             'has 6 intersection(s) with existing showtimes:\n'
                             '1) 31 Dec 1:00–3:29* "Test Film 2:00 hour",\n'
                             '2) 1 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '3) 2 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '4) 3 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '5) 4 Jan 1:00–2:59* "Test Film 1:30 hour",\n'
                             '... and other 1 intersection(s).\n'
                             ' * Attention! Intersections take into account '
                             'the technical break (30 min) after a showtime.')
        self.assertEqual(expected_message, result)

    def test_another_screen(self):
        """
        A new showtime has the same start and end as the existing one,
        but is shown in a different screen.
        [1:00-3:00*) – existing Showtime No.1 {screen: blue}
        [1:00-3:00*) << new test showtime being created {screen: green}.
        * – with technical break after a showtime.
        Should return `None`.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_green,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertIsNone(result)

    def test_when_break_after_showtime_equal_30(self):
        """
        The technical break after a showtime equal 3O minutes.
        The error message must include `(30 min)`.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_phrase = _('technical break (30 min)')
        self.assertTrue(expected_phrase in result)

    def test_when_break_after_showtime_equal_1(self):
        """
        The technical break after a showtime equal 1 minute.
        The error message must include `(1 min)`.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_1
        )
        expected_phrase = _('technical break (1 min)')
        self.assertTrue(expected_phrase in result)

    def test_when_break_after_showtime_equal_0(self):
        """
        The technical break after a showtime equal 0 (zero) minutes.
        The error message must include `(0 min)`.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_0
        )
        not_expected_phrase = _('* Attention! Intersections take into account the technical break')
        not_expected_mark = _('*')
        self.assertTrue(not_expected_phrase not in result)
        self.assertTrue(not_expected_mark not in result)

    def test_has_five_intersections_and_technical_break_equal_3(self):
        """
        New showtimes intersect with existing ones five times.
        [01/01 1:00-3:00*) – existing Showtime No.1
        [01/01 2:00-4:00*) << new test showtime No.1t being created
        …
        [05/01 1:00-3:00*) – existing Showtime No.5
        [05/01 2:00-4:00*) << new test showtime No.5t being created

        At the same time, the argument `show_error` was passed 3.
        Should return an error message with three showtimes.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-05'),
            constants.SCREEN: self.screen_blue,
        }
        result = errors.has_error_intersection_with_existing_showtimes(
            cleaned_form_data,
            self.technical_break_after_showtime_0,
            show_error=3
        )
        expected_message = _('The film distribution that is being created '
                             'has 5 intersection(s) with existing showtimes:\n'
                             '1) 1 Jan 1:00–2:29 "Test Film 1:30 hour",\n'
                             '2) 2 Jan 1:00–2:29 "Test Film 1:30 hour",\n'
                             '3) 3 Jan 1:00–2:29 "Test Film 1:30 hour",\n'
                             '... and other 2 intersection(s).\n')
        self.assertEqual(expected_message, result)
