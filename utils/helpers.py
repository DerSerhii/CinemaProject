"""
The module represents helper functions for use in the project.
"""

import datetime as dt
from collections import namedtuple
from itertools import chain

from django.utils import timezone as tz

from cinema.models import Showtime, ScreenHall, Film


TimeRange = namedtuple('TimeRange', ['start', 'end'])
FilmTimeRange = namedtuple('FilmTimeRange', list(TimeRange._fields) + ['film_name'])


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


def get_technical_break_after_showtime(technical_break: dt.timedelta) -> dt.timedelta:
    """
    Returns passed technical break reduced by one microsecond.

    This solution solves the problem of intersection
    when one showtime ends at a certain time and another showtime starts at the same time.
    It is like a math expression: [start_film, end_film)
    """
    return technical_break - dt.timedelta(microseconds=1)


def get_timerange_new_showtimes(
        film_duration: dt.timedelta,
        start_datetime: dt.datetime,
        last_day: dt.date
) -> list[TimeRange[dt.datetime, dt.datetime, None]]:
    """
    Helper function for forming the time range of new showtimes.
    Returns a list of `TimeRange` namedtuples, consisting of two `datetime.datetime` objects:
    `start` is the beginning of showtime, `end` is its finish.
    """
    time_range_lst = []
    for day in range((last_day - start_datetime.date()).days + 1):
        start = start_datetime + dt.timedelta(days=day)
        end = start + film_duration
        time_range_lst.append(TimeRange(start, end))

    return time_range_lst


def find_showtime_intersections(
        screen: ScreenHall,
        film: Film,
        start_datetime: dt.datetime,
        last_day: dt.date,
        technical_break: dt.timedelta
) -> list[FilmTimeRange[dt.datetime, dt.datetime, str]]:
    """
    The helper function for finding intersections for the film distribution that is being created.

    Returns a list of `FilmTimeRange` namedtuples containing:
    `start` datetime, `end` datetime, and `film_name` string,
    which have intersections with the film distribution that is being created.

    Attention!
    Intersections take into account the technical break after the showtime.
    """
    # Getting showtime ranges that are being created.
    # For each end of showtime, a technical break is added.
    new_showtime_ranges_with_technical_break = list(
        map(
            lambda timerange: timerange._replace(end=timerange.end + technical_break),
            get_timerange_new_showtimes(film.duration, start_datetime, last_day)
        )
    )
    # From the ranges of showtimes,
    # a common list of the starts and ends of these showtimes is created.
    start_end_lst = list(chain.from_iterable(new_showtime_ranges_with_technical_break))

    queryset = Showtime.objects.filter(screen=screen).values_list(
        'start', 'end', 'film__name'
    )
    existing_showtime_ranges = list(map(lambda ft_range: FilmTimeRange._make(ft_range), queryset))

    intersections = []
    for esh_range in existing_showtime_ranges:
        # Converting an aware datetime to local time, since Postgres always returns datetime in UTC.
        start, end = tuple(map(lambda r: tz.localtime(r), (esh_range.start, esh_range.end)))
        # A technical break is added.
        end += technical_break
        if any(start <= start_end <= end for start_end in start_end_lst):
            intersections.append(FilmTimeRange(start, end, esh_range.film_name))

    return intersections
