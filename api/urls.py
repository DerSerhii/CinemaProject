"""
API URL Configuration Module
"""

from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .API.resources import (
    CinemaHomepageAPIView,
    AdminShowtimesAPIView,
    ScreenCinemaViewSet,
    FilmViewSet
)


router = routers.DefaultRouter()
router.register(r'screen-cinema', ScreenCinemaViewSet)
router.register(r'film', FilmViewSet)

urlpatterns = [
    # Authentication URL
    path('token-auth/', views.obtain_auth_token),

    # URL for site visitor
    path('cinema/', CinemaHomepageAPIView.as_view()),

    # URL for custom admin panel
    path('cinema_admin/showtimes/<slug:screen_slug>', AdminShowtimesAPIView.as_view()),

    path('', include(router.urls))
]
