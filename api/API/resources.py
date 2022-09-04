from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.utils import timezone as tz

from api.API.filters import SessionsFilter
from api.API.permissions import IsAdminOrReadOnly
from api.API.serializers import SpectatorSerializer, ScreenCinemaSerializer,\
    ShowtimeSerializers
from cinema.models import Spectator, ScreenCinema, Showtime


class ShowtimeAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ShowtimeViewSet(ReadOnlyModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializers
    filter_backends = (SessionsFilter, )
    pagination_class = ShowtimeAPIListPagination

    def get_queryset(self):
        time_now = tz.localtime(tz.now())
        return Showtime.objects.filter(date__gte=time_now)\
            .exclude(date=time_now, time_start__lte=time_now)

    @action(detail=False, methods=['get'])
    def today(self, request):
        time_now = tz.localtime(tz.now())
        queryset = self.get_queryset().filter(date=time_now, time_start__gt=time_now)
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ScreenCinemaViewSet(ModelViewSet):
    queryset = ScreenCinema.objects.all()
    serializer_class = ScreenCinemaSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = ShowtimeAPIListPagination
