from datetime import datetime, date, timedelta

from django.utils import timezone as tz
from django.test import TestCase

import utils
from cinema_project import settings


class DeriveRangeYearsTestCase(TestCase):
    def setUp(self):
        self.current_year = tz.localtime().year

    def test_default_number_of_years(self):
        expected_years = [self.current_year, self.current_year + 1]
        result = utils.derive_range_years()
        self.assertEqual(result, expected_years)

    def test_custom_number_of_years(self):
        custom_number = 5
        expected_years = [self.current_year + i for i in range(custom_number)]
        result = utils.derive_range_years(custom_number)
        self.assertEqual(result, expected_years)


class ConstructStartDatetimeTestCase(TestCase):
    def test_construct_start_datetime(self):
        test_date = date(2023, 8, 2)
        test_hour = 14
        test_minute = 30
        expected_datetime = tz.make_aware(
            datetime(test_date.year, test_date.month, test_date.day, test_hour, test_minute),
            tz.get_current_timezone()
        )
        result = utils.construct_start_datetime(test_date, test_hour, test_minute)
        self.assertEqual(result, expected_datetime)


class HasErrorShowtimeStartTestCase(TestCase):
    def setUp(self):
        self.now = tz.localtime()
        self.error_message = 'Impossible to create a showtime in the past! %s'

    def test_past_date(self):
        current_date = self.now.date()
        past_date = current_date - timedelta(days=1)
        now_msg = f"Today is {current_date.strftime('%-d %b, %Y')}"
        error_message =  self.error_message % now_msg
        result = utils.has_error_showtime_start(past_date)
        self.assertEqual(error_message, result)

    def test_current_date(self):
        current_date = self.now.date()
        result = utils.has_error_showtime_start(current_date)
        self.assertEqual('', result)

    def test_past_datetime(self):
        current_datetime = self.now
        past_datetime = current_datetime - timedelta(minutes=1)
        now_msg = f"Now: {current_datetime.strftime('%-d %b %H:%M')}"
        error_message = self.error_message % now_msg
        result = utils.has_error_showtime_start(past_datetime)
        self.assertEqual(error_message, result)

    def test_future_datetime(self):
        current_datetime = self.now
        future_datetime = current_datetime + timedelta(minutes=1)
        result = utils.has_error_showtime_start(future_datetime)
        self.assertEqual('', result)

    def test_invalid_input_type(self):
        invalid_input = str(self.now)
        with self.assertRaises(ValueError):
            utils.has_error_showtime_start(invalid_input)


class HasErrorLastDayRentalTestCase(TestCase):
    def setUp(self):
        self.start_day = date(2023, 8, 3)
        self.error_message = "The last day of film rental can't be earlier than the beginning"

    def test_last_day_earlier_than_start(self):
        last_day = date(2023, 8, 2)
        result = utils.has_error_last_day_rental(self.start_day, last_day)
        self.assertEqual(self.error_message, result)

    def test_last_day_same_as_start(self):
        last_day = self.start_day
        result = utils.has_error_last_day_rental(self.start_day, last_day)
        self.assertEqual('', result)

    def test_last_day_later_than_start(self):
        last_day = date(2023, 8, 4)
        result = utils.has_error_last_day_rental(self.start_day, last_day)
        self.assertEqual('', result)


class CalculateShowtimeEndTestCase(TestCase):
    def test_calculate_showtime_end(self):
        start = datetime(2023, 1, 1, 0, 0)
        duration = timedelta(hours=2, minutes=30)
        expected_end = start + duration + settings.TECHNICAL_BREAK_AFTER_SHOWTIME
        result = utils.calculate_showtime_end(start, duration)
        self.assertEqual(expected_end, result)
