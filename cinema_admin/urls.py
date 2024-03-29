"""
The URL Configuration for application `cinema-admin`.
"""

from django.urls import path

from .views import (
    AdminShowtimesView,
    FilmDistributionCreationFormView,
    FilmView,
    ScreenShowtimeView,
    CreateScreenView,
    RemoveScreenView,
    EditScreenView,
    RemoveShowtimeView,
    EditShowtimeView,
    CreateFilmView,
    EditFilmView,
    RemoveFilmView,
    ScreenShowtimeAllView
)

urlpatterns = [
    path('showtimes/<slug:screen_slug>', AdminShowtimesView.as_view(), name='admin-showtimes'),
    path('add-film-distribution/', FilmDistributionCreationFormView.as_view(), name='add-film-distribution'),

    path('films/', FilmView.as_view(), name='film'),
    path('add-film/', CreateFilmView.as_view(), name='add-film'),
    path('edit-film/<int:film_id>/', EditFilmView.as_view(), name='edit-film'),
    path('del-film/<int:film_id>/', RemoveFilmView.as_view(), name='del-film'),
    path('screen/<int:scr_id>/', ScreenShowtimeView.as_view(), name='screen-showtime'),
    path('screen-all/', ScreenShowtimeAllView.as_view(), name='screen-showtime-all'),
    path('add-screen/', CreateScreenView.as_view(), name='add-screen'),
    path('edit-screen/<int:scr_id>/', EditScreenView.as_view(), name='edit-screen'),
    path('del-screen/<int:scr_id>/', RemoveScreenView.as_view(), name='del-screen'),
    path('edit-showtime/<int:show_id>/', EditShowtimeView.as_view(), name='edit-showtime'),
    path('del-showtime/<int:show_id>/', RemoveShowtimeView.as_view(), name='del-showtime'),
]
