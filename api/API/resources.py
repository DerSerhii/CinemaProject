from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CinemaShowtimeSerializer,
    AdminShowtimeSerializer,
    AdminShowtimeContextSerializer,
    ScreenHallSerializer,
    FilmSerializer, FilmDistributionCreationSerializer
)
from cinema.models import ScreenHall, Film
from utils import CinemaShowtimeMixin, AdminShowtimeMixin


class CinemaHomepageAPIView(CinemaShowtimeMixin, ListAPIView):
    """
    API view for retrieving showtime information for cinema homepage.
    Displays films along with today showtimes.
    """
    serializer_class = CinemaShowtimeSerializer

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieves a list of Film objects with their today showtimes and
        adds additional context data to the response under the `context` key.
        """
        response: Response = super().list(request, *args, **kwargs)
        context: dict = self.get_additional_context()
        response.data['context'] = context
        return response


class AdminShowtimesAPIView(AdminShowtimeMixin, ListAPIView):
    """
    API view for managing and displaying showtimes in the custom admin panel.
    """
    serializer_class = AdminShowtimeSerializer

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieves a list of Showtime objects and adds
        additional context data to the response under the `context` key.
        """
        response: Response = super().list(request, *args, **kwargs)
        context: dict = self.get_additional_context()
        response.data['context'] = AdminShowtimeContextSerializer(context).data
        return response


class FilmDistributionCreateAPIView(APIView):
    def post(self, request):
        serializer = FilmDistributionCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Розповсюдження фільму створено'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
