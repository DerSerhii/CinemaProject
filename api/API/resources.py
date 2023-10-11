from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CinemaShowtimeSerializer,
    AdminShowtimeSerializer,
    ScreenHallSerializer,
    FilmSerializer
)
from cinema.models import ScreenHall, Film
from utils import CinemaShowtimeMixin, AdminShowtimeMixin


class CinemaHomepageAPIView(CinemaShowtimeMixin, ListAPIView):
    """
    API view for retrieving showtime information for cinema homepage.
    Displays films along with today showtimes.
    """
    serializer_class = CinemaShowtimeSerializer


class AdminShowtimesAPIView(AdminShowtimeMixin, ListAPIView):
    serializer_class = AdminShowtimeSerializer

    def get_serializer_context(self):
        """
        Adds additional context data to the serializer.
        """
        context = super().get_serializer_context()
        screen_halls = self.get_screen_halls()
        context['selected_day'] = self.selected_day
        context['selected_screen'] = self.kwargs.get('screen_slug')
        context['screens'] = screen_halls
        context['amount_all_showtimes'] = sum([i.amount_showtimes for i in screen_halls])
        return context

class CinemaAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ScreenCinemaViewSet(ModelViewSet):
    queryset = ScreenHall.objects.all()
    serializer_class = ScreenHallSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CinemaAPIListPagination


class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CinemaAPIListPagination
