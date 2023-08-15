"""
This package represents helper functions for use in the project.
"""

from .helpers import (
    TimeRange,
    derive_range_years,
    construct_start_datetime,
    get_technical_break_after_showtime,
    get_time_range_new_showtimes,
    find_showtime_intersections
)
from .errors import (
    has_error_showtime_start,
    has_error_last_day_distribution,
    has_error_intersection_with_existing_showtime,
)

__all__ = [
    'TimeRange',
    'derive_range_years',
    'construct_start_datetime',
    'get_technical_break_after_showtime',
    'get_time_range_new_showtimes',
    'find_showtime_intersections',
    'has_error_showtime_start',
    'has_error_last_day_distribution',
    'has_error_intersection_with_existing_showtime'
]
