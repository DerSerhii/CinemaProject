import datetime as dt
from itertools import groupby

from django.db.models import Count, Q, QuerySet
from django.utils import timezone as tz

from cinema.models import Film, Showtime, ScreenHall


class ShowtimeMixin:
    """
    Mixin class for processing showtime-related queries.

    This mixin provides methods to process GET requests, retrieve the selected day,
    and set up showtime filters for queries.

    It is designed to be used in views that display showtime-related information.
    """

    def get(self, request, *args, **kwargs):
        """
        Processes the GET request and set up filter settings for showtime queries.

        This method is overridden to provide custom filter settings for showtime queries.
        It initializes the current moment, retrieves the selected day,
        and sets up two different showtime filters:
        one for direct use in the `Showtime` model, and another for use in related models.
        """
        self._current_moment = tz.localtime()
        self.selected_day = self.get_selected_day()
        self.showtime_filter_direct, self.showtime_filter_related = self.set_showtime_filter_settings()
        return super().get(request, *args, **kwargs)

    def get_selected_day(self) -> dt.date:
        """
        Gets the selected day based on the `day` query parameter in the request.

        If the `day` parameter is provided in the request, it parses the date
        from the parameter and returns it as a `datetime.date` object.
        If the `day` parameter is not provided, it returns the current date as obtained
        from the '_current_moment' attribute.

        :return: A `datetime.date` object representing the selected day.
        """
        if day := self.request.GET.get('day'):
            return tz.datetime.strptime(day, "%m/%d/%Y").date()
        return self._current_moment.date()

    def set_showtime_filter_settings(self) -> tuple[Q, Q]:
        """
        Setting the showtime filters based on the selected day.

        :return: A tuple containing two showtime filters.
        The first filter is for direct use in the Showtime model,
        and the second filter is for use in related models.
        """
        selected_day = self.selected_day
        current_moment = self._current_moment
        today = current_moment.date()

        showtime_filter_direct = Q(start__date=selected_day)
        showtime_filter_related = Q(showtime__start__date=selected_day)

        if today == selected_day:
            showtime_filter_direct &= Q(start__gte=current_moment)
            showtime_filter_related &= Q(showtime__start__gte=current_moment)

        return showtime_filter_direct, showtime_filter_related

    def get_showtime_queryset(self) -> QuerySet[Showtime]:
        """
        Retrieves a queryset of Showtime objects.
        This method returns a queryset of Showtime objects, optimized for database queries.

        :return: A QuerySet containing Showtime objects matching the specified filter criteria.
        """
        return (
            Showtime.objects.select_related('film', 'screen')
            .defer(
                'end',
                'price',
                'attendance',
                'film__duration',
                'film__is_active',
                'film__release_year',
                'screen__slug',
                'screen__capacity'
            )
            .filter(self.showtime_filter_direct)
        )

    def get_additional_context(self) -> dict:
        """
        Retrieves and returns a dictionary with additional context data.
        """
        return dict(selected_day=self.selected_day)


class CinemaShowtimeMixin(ShowtimeMixin):
    """
    Mixin class for handling showtime-related operations in a cinema application.

    This mixin extends the `ShowtimeMixin` and provides additional functionality
    for retrieving a list of films along with their showtimes for display on a cinema website.

    It includes methods for setting filter settings based on the selected day,
    and for retrieving films, and their showtimes for the selected day.
    """

    def get_queryset(self) -> list[tuple[Film, list[Showtime]]]:
        """
        Retrieves a list of films along with their showtimes for display on the page.

        This method constructs a list of tuples, where each tuple contains a Film object
        and a list of Showtime objects.
        The Showtime objects are grouped by their associated Film.
        It returns this list to provide data for the view.

        :return: A list of tuples, each containing a Film object,
        and a list of associated Showtime objects.
        """
        showtime_queryset = self.get_showtime_queryset()

        sorted_showtimes = sorted(showtime_queryset, key=lambda f: f.film_id)
        context_films = []
        for film, showtimes in groupby(sorted_showtimes, key=lambda sh: sh.film):
            context_films.append((film, list(showtimes)))
        return context_films


class AdminShowtimeMixin(ShowtimeMixin):
    """
    Mixin class for handling showtime-related operations in the cinema admin panel.

    This mixin extends the `ShowtimeMixin` and provides additional functionality
    for retrieving a filtered queryset of Showtime objects based on the selected screen slug
    for the cinema admin panel.

    It includes methods for setting filter settings based on the selected day,
    and for retrieving a filtered queryset of Showtime objects.
    """

    def get_queryset(self) -> QuerySet[Showtime]:
        """
        Retrieves a filtered queryset of Showtime objects based on the selected screen slug.

        This method gets the initial queryset of Showtime objects.
        It then filters the queryset based on the provided `screen_slug` parameter from the URL.
        If the `screen_slug` is not `all`, it filters the queryset
        to include only Showtimes associated with the specified screen.
        If 'screen_slug' is 'all', the full queryset is returned.

        :return: A filtered queryset of Showtime objects.
        """
        queryset = self.get_showtime_queryset()

        screen_slug = self.kwargs.get('screen_slug')
        if screen_slug != 'all':
            return queryset.filter(screen__slug=screen_slug)
        return queryset

    def get_screen_halls_queryset(self) -> QuerySet[ScreenHall]:
        """
        Retrieves and returns information about all screening halls (ScreenHall)
        along with a count of associated Showtime instances for each hall.
        """
        return (
            ScreenHall.objects.annotate(
                amount_showtimes=Count('showtime', filter=self.showtime_filter_related)
            )
            .defer('capacity')
        )

    def get_additional_context(self) -> dict:
        """
        Retrieves and returns a dictionary with additional context data.
        """
        screen_halls = self.get_screen_halls_queryset()
        amount_all_showtimes = sum([hall.amount_showtimes for hall in screen_halls])
        additional_context = super().get_additional_context()
        additional_context.update(
            {
                'selected_screen': self.kwargs.get('screen_slug'),
                'screens': screen_halls,
                'amount_all_showtimes': amount_all_showtimes
            }
        )
        return additional_context
