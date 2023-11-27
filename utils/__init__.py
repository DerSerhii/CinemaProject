"""
This package represents helper functions and mixins for use in the project.
"""

from .helpers import (
    TimeRange, FilmTimeRange,
    derive_range_years,
    construct_start_datetime,
    get_technical_break_after_showtime,
    get_timerange_new_showtimes,
    find_showtime_intersections
)
from .errors import (
    has_showtime_creation_error_in_past,
    has_error_last_day_distribution,
    has_error_intersection_with_existing_showtimes,
)
from .mixins import CinemaShowtimeMixin, AdminShowtimeMixin
from .validators import FilmDistributionCreationValidator


__all__ = [
    'FilmDistributionCreationValidator',
    'TimeRange', 'FilmTimeRange',
    'derive_range_years',
    'construct_start_datetime',
    'get_technical_break_after_showtime',
    'get_timerange_new_showtimes',
    'find_showtime_intersections',
    'has_error_last_day_distribution',
    'has_error_intersection_with_existing_showtimes',
    'CinemaShowtimeMixin',
    'AdminShowtimeMixin'
]
