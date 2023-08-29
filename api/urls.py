from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from api.API.resources import ScreenCinemaViewSet, ShowtimeViewSet, FilmViewSet

router = routers.SimpleRouter()
router.register(r'screen-cinema', ScreenCinemaViewSet)
router.register(r'film', FilmViewSet)
router.register(r'showtime', ShowtimeViewSet)

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
