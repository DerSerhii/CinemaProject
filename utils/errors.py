"""
The module represents helper functions that provide error messages
for various actions used in the project.
"""

import datetime as dt

from django.utils import timezone as tz

from cinema.models import ScreenCinema, Film
from .helpers import find_showtime_intersections


def has_error_showtime_start(start: dt.datetime | dt.date) -> str | None:
    """
    Returns an error message if the start of showtime less than the current moment.
    If there is no error returns `None`.
    """
    if type(start) == dt.date:
        now = tz.localdate()
        now_msg = f"Today is {now.strftime('%-d %b, %Y')}"
    elif type(start) == dt.datetime:
        now = tz.localtime()
        now_msg = f"Now: {now.strftime('%-d %b %H:%M')}"
    else:
        raise ValueError(f"Passed {type(start)} but must be 'datetime.date' "
                         "or 'datetime.datetime' object")
    if start < now:
        return 'Impossible to create a showtime in the past! %s' % now_msg


def has_error_last_day_distribution(start: dt.date, last: dt.date) -> str:
    """
    Returns an error message if the last day of distribution film is earlier than the beginning.
    If there is no error returns `None`.
    """
    if last < start:
        return "The last day of film distribution can't be earlier than the beginning"


def has_error_intersection_with_existing_showtime(
        screen: ScreenCinema,
        film: Film,
        start_datetime: dt.datetime,
        last_day: dt.date,
        quantity: int = 5
    ) -> str | None:
    """
    Returns an error message if the created film distribution has intersections
    with existing showtime.
    If there is no error returns an empty list.
    """
    if intersections := find_showtime_intersections(screen, film, start_datetime, last_day):
        error_message = ('The film distribution that is being created '
                         f'has {len(intersections)} intersection(s) with existing showtime: ')
        for i, intersect in enumerate(intersections, start=1):
            start = intersect[0].strftime('%-d %b %H:%M')
            end = intersect[1].strftime('%H:%M')
            punctuation_mark = ',' if len(intersections) > 1 else '.'
            error_message += f"<{start}-{end} '{intersect[2]}'>{punctuation_mark} "
            if i >= quantity:
                error_message += '...'
                break
        return error_message
