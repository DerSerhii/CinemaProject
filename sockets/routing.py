from django.urls import path

from .consumers import NowShowtimesPlayingConsumer, ChatConsumer


websocket_urlpatterns = [
    path('ws/now_showtime_playing/', NowShowtimesPlayingConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi(), name='room'),
]
