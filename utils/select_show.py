import datetime as dt

from django.db.models import Q
from django.utils import timezone as tz

from cinema.models import Showtime, Film


def get_selected_day(query_date: str) -> dt.datetime:
    """
    Return selected day from template or today if start page
    """
    if query_date:
        showtime_day = dt.datetime.strptime(query_date, "%m/%d/%Y")
    else:
        showtime_day = tz.localtime(tz.now())

    return showtime_day


def get_films_with_showtimes_on_this_day(select_day):
    """
    Returns a list of Films with QuerySets of Showtimes on this day
    """

    # get films on this day
    query_film_on_this_day = \
        Showtime.objects.values("film").filter(date=select_day).distinct()

    list_film_id_on_this_day = [i.get("film") for i in query_film_on_this_day]

    # get films with showtimes on this day
    films_with_showtime_on_this_day = []

    q_select_day = Q(date=select_day)
    q_time_start_gte_now = Q(time_start__gte=tz.localtime(tz.now()).time())

    if select_day == tz.localtime(tz.now()).date():
        q_filter = q_select_day & q_time_start_gte_now
    else:
        q_filter = q_select_day

    for film_id in list_film_id_on_this_day:
        film = Film.objects.get(id=film_id). \
            showtime_set.filter(q_filter).order_by("time_start")
        films_with_showtime_on_this_day.append(film)

        return films_with_showtime_on_this_day
