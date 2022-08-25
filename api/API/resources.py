from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.API.permissions import IsAdminOrReadOnly
from api.API.serializers import SpectatorSerializer, ScreenCinemaSerializer
from cinema.models import Spectator, ScreenCinema


class ShowtimeAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class ScreenCinemaViewSet(ModelViewSet):
    queryset = ScreenCinema.objects.all()
    serializer_class = ScreenCinemaSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = ShowtimeAPIListPagination
