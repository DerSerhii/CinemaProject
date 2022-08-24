from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from api.API.resources import ScreenCinemaViewSet


router = routers.SimpleRouter()
router.register('screen-cinema', ScreenCinemaViewSet)


urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
