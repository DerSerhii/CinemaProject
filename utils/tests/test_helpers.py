"""
The module represents test cases for functions of module `helpers`.
"""

import datetime as dt

from django.test import TestCase
from django.utils import timezone as tz

from utils import helpers
from cinema_project import constants
from cinema.models import ScreenHall, Film, Showtime


class DeriveRangeYearsTestCase(TestCase):
    """
    Test case for the `derive_range_years` function.
    """

    def setUp(self):
        self.current_year = tz.localtime().year

    def test_default_number_of_years(self):
        expected_years = [self.current_year, self.current_year + 1]
        result = helpers.derive_range_years()
        self.assertEqual(result, expected_years)

    def test_custom_number_of_years(self):
        custom_number = 5
        expected_years = [self.current_year + i for i in range(custom_number)]
        result = helpers.derive_range_years(custom_number)
        self.assertEqual(result, expected_years)


class ConstructStartDatetimeTestCase(TestCase):
    """
    Test case for the `construct_start_datetime` function.
    """

    def test_construct_start_datetime(self):
        test_date = dt.date(2023, 8, 2)
        test_hour = 14
        test_minute = 30
        expected_datetime = tz.make_aware(
            dt.datetime(test_date.year, test_date.month, test_date.day, test_hour, test_minute),
            tz.get_current_timezone()
        )
        result = helpers.construct_start_datetime(test_date, test_hour, test_minute)
        self.assertEqual(result, expected_datetime)


class GetTimeRangeNewShowtimesTestCase(TestCase):
    """
    Test case for the `get_time_range_new_showtimes` function.
    """

    def setUp(self):
        self.film_1_30 = Film.objects.create(
            name='Test Film 1:30 hour',
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
            duration=dt.timedelta(hours=1)
        )

    def test_single_showtime(self):
        """
        A single showtime is created.
        The end of the showtime should be equal to the beginning plus the length of the film.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00')
        last_day = dt.date.fromisoformat('2023-01-01')
        result = helpers.get_timerange_new_showtimes(
            self.film_1_30.duration,
            start_datetime,
            last_day
        )
        expected_data = [
            (
                start_datetime,
                dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00')
            )
        ]
        self.assertEqual(1, len(result))
        self.assertEqual(list, type(result))
        self.assertEqual(helpers.TimeRange, type(result[0]))
        self.assertEqual(dt.datetime, type(result[0].start))
        self.assertEqual(dt.datetime, type(result[0].end))
        self.assertEqual(expected_data, result)

    def test_film_distribution(self):
        """
        Showtimes are created from 01/01 to 04/01.
        There should be four showtimes in total, which start at the same time each of these days.
        """
        start_datetime_release = dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00')
        start_datetime_day_3 = dt.datetime.fromisoformat('2023-01-03 01:00:00+02:00')
        last_day = dt.date.fromisoformat('2023-01-04')
        result = helpers.get_timerange_new_showtimes(
            self.film_1_30.duration,
            start_datetime_release,
            last_day
        )
        expected_data = [
            (
                start_datetime_release,
                dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00')
            ),
            (
                start_datetime_release + dt.timedelta(days=1),
                dt.datetime.fromisoformat('2023-01-02 02:00:00+02:00')
            ),
            (
                start_datetime_day_3,
                start_datetime_day_3 + self.film_1_30.duration
            ),
            (
                dt.datetime.fromisoformat('2023-01-04 01:00:00+02:00'),
                dt.datetime.fromisoformat('2023-01-04 02:00:00+02:00')
            ),
        ]
        self.assertEqual(4, len(result))
        self.assertEqual(expected_data, result)


class TestParseCleanedData(TestCase):
    """
    Test case for the `parse_cleaned_data` function.
    """

    def setUp(self):
        self.screen_blue = ScreenHall.objects.create(name='blue', capacity=50)
        film_duration = dt.timedelta(hours=1.5)
        self.film_1_30 = Film.objects.create(
            title='Test Film 1:30 hour',
            duration=film_duration,
            release_year=2023,
            description='Test Description',
            starring='Test Starring',
            director='Test Director',
        )
        self.start_datetime = dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00')
        self.showtime = Showtime.objects.create(
            film=self.film_1_30,
            start=self.start_datetime,
            end=self.start_datetime + film_duration,
            screen=self.screen_blue
        )

    def test_valid_data_with_showtime(self):
        """
        Test with incoming cleaned data:
        'showtime', 'start_datetime', 'screen'
        """
        cleaned_data = {
            constants.SHOWTIME: self.showtime,
            constants.START_DATETIME: self.start_datetime,
            constants.SCREEN: self.screen_blue,
        }

        result = helpers.parse_cleaned_data(cleaned_data)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 5)
        self.assertIsInstance(result[0], Film)
        self.assertIsInstance(result[1], dt.datetime)
        self.assertIsInstance(result[2], dt.date)
        self.assertIsInstance(result[3], ScreenHall)
        self.assertIsInstance(result[4], int)

    def test_valid_data_with_film(self):
        """
        Test with incoming cleaned data:
        'film', 'start_datetime', 'last_day', 'screen'
        """
        cleaned_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: self.start_datetime,
            constants.LAST_DAY: self.start_datetime.date(),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.parse_cleaned_data(cleaned_data)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 5)
        self.assertIsInstance(result[0], Film)
        self.assertIsInstance(result[1], dt.datetime)
        self.assertIsInstance(result[2], dt.date)
        self.assertIsInstance(result[3], ScreenHall)
        self.assertIsNone(result[4])

    def test_missing_start_datetime(self):
        """
        Test with incoming cleaned data: 'showtime', 'screen'
        and missing 'start_datetime'.
        """
        cleaned_data = {
            constants.SHOWTIME: self.showtime,
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(KeyError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_missing_screen(self):
        """
        Test with incoming cleaned data: 'showtime', 'start_datetime'
        and missing 'screen'.
        """
        cleaned_data = {
            constants.SHOWTIME: self.showtime,
            constants.START_DATETIME: self.start_datetime,
        }
        with self.assertRaises(KeyError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_missing_last_day(self):
        """
        Test with incoming cleaned data: 'film', 'start_datetime', 'screen'
        and missing 'last_day'.
        """
        cleaned_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: self.start_datetime,
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(KeyError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_missing_showtime_and_film(self):
        """
        Test with incoming cleaned data: 'start_datetime', 'screen'
        and missing 'showtime' and 'film'.
        """
        cleaned_data = {
            constants.START_DATETIME: self.start_datetime,
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(KeyError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_invalid_start_datetime_type(self):
        """
        Test with invalid type `start_datetime` value.
        """
        cleaned_data = {
            constants.SHOWTIME: self.showtime,
            constants.START_DATETIME: self.start_datetime.date(),  # invalid: must be dt.datetime
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(TypeError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_invalid_last_day_type(self):
        """
        Test with invalid type `last_day` value.
        """
        cleaned_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: self.start_datetime,
            constants.LAST_DAY: self.start_datetime,  # invalid: must be dt.date
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(TypeError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_invalid_screen_type(self):
        """
        Test with invalid type `screen` value.
        """
        cleaned_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: self.start_datetime,
            constants.LAST_DAY: self.start_datetime.date(),
            constants.SCREEN: self.film_1_30,  # invalid: must be ScreenHall
        }
        with self.assertRaises(TypeError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_invalid_showtime_type(self):
        """
        Test with invalid type `showtime` value.
        """
        cleaned_data = {
            constants.SHOWTIME: self.film_1_30,  # invalid: must be Showtime
            constants.START_DATETIME: self.start_datetime,
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(TypeError):
            helpers.parse_cleaned_data(cleaned_data)

    def test_invalid_film_type(self):
        """
        Test with invalid type `film` value.
        """
        cleaned_data = {
            constants.FILM: self.showtime,  # invalid: must be Film
            constants.START_DATETIME: self.start_datetime,
            constants.LAST_DAY: self.start_datetime.date(),
            constants.SCREEN: self.screen_blue,
        }
        with self.assertRaises(TypeError):
            helpers.parse_cleaned_data(cleaned_data)


class FindShowtimeIntersectionsTestCase(TestCase):
    """
    Test case for the `find_showtime_intersections` function.
    """

    def setUp(self):
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
        # Showtime_No.1 [01/01 1:00-2:30]
        self.start_datetime_sw1 = dt.datetime.fromisoformat('2023-01-01 01:00:00+02:00')
        Showtime.objects.create(
            film=self.film_1_30,
            start=self.start_datetime_sw1,
            end=self.start_datetime_sw1 + film_duration,
            screen=self.screen_blue
        )
        # Showtime_No.2 [01/01 5:00-6:30]
        self.start_datetime_sw2 = dt.datetime.fromisoformat('2023-01-01 05:00:00+02:00')
        Showtime.objects.create(
            film=self.film_1_30,
            start=self.start_datetime_sw2,
            end=self.start_datetime_sw2 + film_duration,
            screen=self.screen_blue
        )
        # Showtime_No.1_2 [02/01 1:00-2:30]
        self.start_datetime_sw1_2 = dt.datetime.fromisoformat('2023-01-02 01:00:00+02:00')
        Showtime.objects.create(
            film=self.film_1_30,
            start=self.start_datetime_sw1_2,
            end=self.start_datetime_sw1_2 + film_duration,
            screen=self.screen_blue
        )
        # Showtime_No.1_3 [02/01 1:00-2:30]
        self.start_datetime_sw1_3 = dt.datetime.fromisoformat('2023-01-03 01:00:00+02:00')
        Showtime.objects.create(
            film=self.film_1_30,
            start=self.start_datetime_sw1_3,
            end=self.start_datetime_sw1_3 + film_duration,
            screen=self.screen_blue
        )

        # *************************** Technical Break Set ******************************
        self.technical_break_after_showtime_30 = helpers.get_technical_break_after_showtime(
            dt.timedelta(minutes=30)
        )
        self.technical_break_after_showtime_0 = helpers.get_technical_break_after_showtime(
            dt.timedelta(minutes=0)
        )

    def test_no_intersections(self):
        """
        A new showtime is strictly between two existing showtimes.
        [1:00-3:00*) – existing Showtime No.1
        [3:00-5:00*) << new test showtime being created
        [5:00-7:00*) – existing Showtime No.2
        * – with technical break after a showtime.
        Should not have showtime intersections.
        """
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: dt.datetime.fromisoformat('2023-01-01 03:00:00+02:00'),
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertEqual([], result)

    def test_showtime_similar_to_existing_showtime(self):
        """
        A new showtime has the same start and end as the existing one.
        [1:00-3:00*) – existing Showtime No.1
        [1:00-3:00*) << new test showtime being created.
        * – with technical break after a showtime.
        There must be an intersection.
        """
        start_datetime = self.start_datetime_sw1
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        expected_data = [
            (
                start_datetime,
                start_datetime + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_showtime_start_similar_to_existing_showtime(self):
        """
        A new showtime has the same start as the existing one.
        [1:00-3:00*) – existing Showtime No.1
        [1:00-3:30*) << new test showtime being created.
        * – with technical break after a showtime.
        There must be an intersection.
        """
        start_datetime = self.start_datetime_sw1
        cleaned_form_data = {
            constants.FILM: self.film_2_00,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertTrue(result)
        expected_data = [
            (
                start_datetime,
                start_datetime + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_showtime_start_intersect_existing_showtime(self):
        """
        A new showtime has start among an existing showtime.
        [1:00-3:00*) – existing Showtime No.1.
        [2:00-4:00*) << new test showtime being created.
        * – With technical break after a showtime.
        There must be an intersection.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertTrue(result)
        expected_data = [
            (
                self.start_datetime_sw1,
                self.start_datetime_sw1 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_showtime_end_intersect_existing_showtime(self):
        """
        A new showtime has the end among an existing showtime.
        [4:00-6:00*) << new test showtime being created.
        [5:00-7:00*) – existing Showtime No.2.
        * – with technical break after a showtime.
        There must be an intersection.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 04:00:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertTrue(result)
        expected_data = [
            (
                self.start_datetime_sw2,
                self.start_datetime_sw2 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_showtime_start_in_last_year_and_end_intersect_existing_showtime(self):
        """
        A new showtime starts in last (year, month, day) and has the end among an existing showtime.
        [31/12 23:00 – 01/01 1:30*) << new test showtime being created.
        [01/01 1:00–3:00*) – existing Showtime No.1.
        * – with technical break after a showtime.
        There must be an intersection.
        """
        start_datetime = dt.datetime.fromisoformat('2022-12-31 23:00:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_2_00,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2022-12-31'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertTrue(result)
        expected_data = [
            (
                self.start_datetime_sw1,
                self.start_datetime_sw1 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_showtime_start_and_end_intersect_existing_showtimes(self):
        """
        A new showtime has the start and the end among an existing showtime.
        [1:00-3:00*) – existing Showtime No.1.
        [2:45-5:15*) << new test showtime being created.
        [5:00-7:00*) – existing Showtime No.2.
        * – with technical break after a showtime.
        There must be two intersections.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 02:45:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_2_00,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertEqual(2, len(result))
        expected_data = [
            (
                self.start_datetime_sw1,
                self.start_datetime_sw1 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            ),
            (
                self.start_datetime_sw2,
                self.start_datetime_sw2 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_film_distribution_start_intersect_existing_showtimes(self):
        """
        A new film distribution has the start among an existing showtimes.
        [01/01 1:00-3:00*) – existing Showtime No.1.
        [01/01 2:00-4:00*) << new test showtime being created No.1.
        [02/01 1:00-3:00*) – existing Showtime No.1_2.
        [02/01 2:00-4:00*) << new test showtime being created No.2.
        [03/01 1:00-3:00*) – existing Showtime No.1_3.
        [03/01 2:00-4:00*) << new test showtime being created No.3.
        There must be three intersections.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 02:00:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-03'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertEqual(3, len(result))
        expected_data = [
            (
                self.start_datetime_sw1,
                self.start_datetime_sw1 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            ),
            (
                self.start_datetime_sw1_2,
                self.start_datetime_sw1_2 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            ),
            (
                self.start_datetime_sw1_3,
                self.start_datetime_sw1_3 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_film_distribution_end_intersect_existing_showtimes(self):
        """
        A new film distribution has the end among an existing showtimes.
        [31/12 23:00 – 01/01 1:30*) << new test showtime being created No.1.
        [01/01 1:00-3:00*) – existing Showtime No.1.
        [01/01 23:00 – 02/01 1:30*) << new test showtime being created No.2.
        [02/01 1:00-3:00*) – existing Showtime No.1_2.
        [02/01 23:00 – 03/01 1:30*) << new test showtime being created No.2.
        [03/01 1:00-3:00*) – existing Showtime No.1_3.
        There must be three intersections.
        """
        start_datetime = dt.datetime.fromisoformat('2022-12-31 23:00:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_2_00,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-03'),
            constants.SCREEN: self.screen_blue,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertEqual(3, len(result))
        expected_data = [
            (
                self.start_datetime_sw1,
                self.start_datetime_sw1 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            ),
            (
                self.start_datetime_sw1_2,
                self.start_datetime_sw1_2 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            ),
            (
                self.start_datetime_sw1_3,
                self.start_datetime_sw1_3 + self.film_1_30.duration + self.technical_break_after_showtime_30,
                self.film_1_30.title
            )
        ]
        self.assertEqual(expected_data, result)

    def test_another_screen(self):
        """
        A new showtime has the same start and end as the existing one,
        but is shown in a different screen.
        [1:00-3:00*) – existing Showtime No.1 {screen: blue}
        [1:00-3:00*) << new test showtime being created {screen: green}.
        * – With technical break after a showtime.
        Should not have showtime intersections.
        """
        start_datetime = self.start_datetime_sw1
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_green,
        }
        result = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_30
        )
        self.assertEqual([], result)

    def test_when_break_after_showtime_equal_zero(self):
        """
        The technical break after a showtime equal O (zero) minutes.
        [1:00-2:30*) – existing Showtime No.1
        [2:30-4:00*) << new test showtime being created.
        * – technical break after a showtime should still have minus one microsecond.
        Should not have showtime intersections.
        """
        start_datetime = dt.datetime.fromisoformat('2023-01-01 02:30:00+02:00')
        cleaned_form_data = {
            constants.FILM: self.film_1_30,
            constants.START_DATETIME: start_datetime,
            constants.LAST_DAY: dt.date.fromisoformat('2023-01-01'),
            constants.SCREEN: self.screen_blue,
        }
        result_1_30 = helpers.find_showtime_intersections(
            cleaned_form_data,
            self.technical_break_after_showtime_0
        )
        self.assertEqual([], result_1_30)
