from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CinemaShowtimeSerializer,
    AdminShowtimeSerializer,
    AdminShowtimeContextSerializer,
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
    """
    API view for managing and displaying showtimes in the custom admin panel.
    """
    serializer_class = AdminShowtimeSerializer

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieves a list of Showtime objects and adds
        additional context data to the response.

        This method first calls the parent class's `list` method
        to retrieve a list of Showtime objects.
        It then obtains additional context data and includes this data
        in the response under the `context` key.

        """
        response: Response = super().list(request, *args, **kwargs)
        context: dict = self.get_context()
        response.data['context'] = AdminShowtimeContextSerializer(context).data
        return response


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
