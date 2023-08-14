from datetime import date, timedelta

from django.utils import timezone as tz
from django.test import TestCase

import utils


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
        self.assertEqual(None, result)

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
        self.assertEqual(None, result)

    def test_invalid_input_type(self):
        invalid_input = str(self.now)
        with self.assertRaises(ValueError):
            utils.has_error_showtime_start(invalid_input)


class HasErrorLastDayDistributionTestCase(TestCase):
    def setUp(self):
        self.start_day = date(2023, 8, 3)
        self.error_message = "The last day of film distribution can't be earlier than the beginning"

    def test_last_day_earlier_than_start(self):
        last_day = date(2023, 8, 2)
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(self.error_message, result)

    def test_last_day_same_as_start(self):
        last_day = self.start_day
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(None, result)

    def test_last_day_later_than_start(self):
        last_day = date(2023, 8, 4)
        result = utils.has_error_last_day_distribution(self.start_day, last_day)
        self.assertEqual(None, result)
