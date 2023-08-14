"""
The module represents helper functions for use in the project.
"""

import datetime as dt

from django.utils import timezone as tz

from cinema.models import Showtime, ScreenCinema, Film
from cinema_project import settings


def derive_range_years(quantity: int = 2) -> list[int]:
    """
    Returns a list of consecutive years starting with the current year.
    The number of years is determined by the parameter `quantity` by default 2.
    """
    current_year: int = tz.localtime().year
    return [current_year + i for i in range(quantity)]


def construct_start_datetime(start_day: dt.date,
                             start_hour: int,
                             start_minute: int) -> tz.datetime:
    """
    Constructs a timezone-aware datetime object based on the provided
    start day, start hour, and start minute.
    """
    start_time = dt.time(hour=start_hour, minute=start_minute)
    return tz.make_aware(dt.datetime.combine(start_day, start_time))


def calculate_showtime_end(start: dt.datetime, duration: dt.timedelta) -> dt.datetime:
    """
    TODO remove
    Returns a calculated end datetime for a showtime based on passed start and duration.
    Also, showtime includes technical break after a showtime.
    """
    return start + duration + settings.TECHNICAL_BREAK_AFTER_SHOWTIME


def find_showtime_intersections(
        screen: ScreenCinema,
        film: Film,
        start_datetime: tz.datetime,
        last_day: dt.date,
        technical_break: dt.timedelta
    ) -> list[tuple[dt.datetime, dt.datetime, str]]:
    """
    The helper function for finding intersections for the created film distribution.
    Returns a list of tuples containing a start datetime, an end datetime, and a film title(name)
    that have intersections with the created film distribution.
    """
    finish_datetime = start_datetime + film.duration + technical_break

    start_end_lst = []
    for day in range((last_day - start_datetime.date()).days + 1):
        start_end_lst += list(
            map(lambda x: x + dt.timedelta(days=day), (start_datetime, finish_datetime))
        )

    existing_showtime_ranges = Showtime.objects.filter(screen=screen).values_list(
        'start', 'end', 'film__name'
    )
    intersections = []
    for esr in existing_showtime_ranges:
        start, end = tuple(map(lambda x: tz.localtime(x), (esr[0], esr[1])))
        end += technical_break
        if any(start <= start_end <= end for start_end in start_end_lst):
            intersections.append((start, end, esr[2]))

    return intersections
