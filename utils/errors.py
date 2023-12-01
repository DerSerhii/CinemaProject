"""
The module represents helper functions that provide error messages
for various actions used in the project.
"""

import datetime as dt

from django.utils import timezone as tz
from django.utils.translation import gettext as _

from cinema.models import ScreenHall, Film
from .helpers import find_showtime_intersections


def has_showtime_creation_error_in_past(start: dt.datetime | dt.date) -> str | None:
    """
    Returns an error message if the start of showtime less than the current moment.
    If there is no error, returns `None`.
    """
    if type(start) == dt.date:
        now = tz.localdate()
        now_msg = f"Today's already {now.strftime('%-d %b, %Y')}"
    elif type(start) == dt.datetime:
        now = tz.localtime()
        now_msg = f"Now's {now.strftime('%H:%M')}"
    else:
        raise ValueError(f"Passed {type(start)} but must be 'datetime.date' "
                         "or 'datetime.datetime' object")
    if start < now:
        return _('Impossible to create a showtime in the past! %s' % now_msg)


def has_error_last_day_distribution(start: dt.date, last: dt.date) -> str | None:
    """
    Returns an error message if the last day of distribution film is earlier than the beginning.

    If there is no error, returns `None`.
    """
    if last < start:
        return _("The last day of film distribution can't be earlier than the beginning")


def has_error_intersection_with_existing_showtimes(
        cleaned_form_data: dict,
        technical_break: dt.timedelta,
        show_error: int = 5) -> str | None:
    """
    Returns an error message if film distribution that is being created has intersections
    with existing showtimes.

    Attention!
    Intersections take into account the technical break after the showtime.

    If there is no error, returns `None`.
    """
    intersections = find_showtime_intersections(cleaned_form_data, technical_break)
    quantity_intersections = len(intersections)

    if intersections:
        error_message = _('The film distribution that is being created '
                          f'has {quantity_intersections} intersection(s) with existing showtimes:\n')
        break_mark = break_note = ''

        for i, intersect in enumerate(intersections, start=1):
            start = intersect.start.strftime('%-d %b %-H:%M')
            end = intersect.end.strftime('%-H:%M')
            punctuation_mark = ',' if i != quantity_intersections else '.'

            if technical_break > dt.timedelta():
                break_mark = '*'
                break_note = _(' * Attention! Intersections take into account the technical break '
                               f'({technical_break.seconds // 60 + 1} min) after a showtime.')

            error_message += (
                _(f'{i}) {start}–{end}{break_mark} "{intersect.film_name}"{punctuation_mark}\n')
            )

            if i >= show_error and i != quantity_intersections:
                error_message += _(f'... and other {quantity_intersections - i} intersection(s).\n')
                break

        error_message += break_note

        return error_message
