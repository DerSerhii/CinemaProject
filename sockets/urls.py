from django.urls import path

from .views import ChatView, FilmChatView

urlpatterns = [
    path('', ChatView.as_view(), name='index'),
    path('<str:room_name>/', FilmChatView.as_view(), name='room'),
]
