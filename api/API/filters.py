from rest_framework import filters


class SessionsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        screen = request.query_params.get("screen")
        start_between = request.query_params.get("start_between")
        if screen:
            queryset = queryset.filter(screen__name=screen.lower())
        if start_between:
            start_between = start_between.split("-")
            queryset = queryset.filter(time_start__gte=start_between[0],
                                       time_start__lte=start_between[1])
        return queryset
