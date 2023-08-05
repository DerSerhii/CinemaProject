"""
The module represents template tag providing a week period starting from the current date.
"""
from datetime import date, timedelta

from django.utils import timezone as tz
from django import template

register = template.Library()

@register.simple_tag
def get_week_period() -> list[date]:
    """
    Provides template tag that returns a list of dates representing a week period starting
    from the current date (including today and the next six days).
    """
    today = tz.localdate()
    return [today + timedelta(days=i) for i in range(7)]
