from datetime import timedelta

from django.utils import timezone as tz
from django import template

register = template.Library()
now = tz.now()


@register.simple_tag
def get_week():
    week = []

    for day in range(7):
        day = tz.localtime(now).date() + timedelta(day)
        week.append(day)

    return week
