"""The URL Configuration of application CINEMA"""

from django.urls import path

from .views import CinemaHomeView, SignUpView, SignInView, Logout, ProfileSpectatorView, \
    WalletSpectatorView, ShowtimeView, BuyTicketView, SpectatorPurchaseView

urlpatterns = [
    path('', CinemaHomeView.as_view(), name='cinema-home'),
    path('showtime/<int:show_id>', ShowtimeView.as_view(), name='showtime'),
    path('showtime/<int:show_id>/buy-ticket', BuyTicketView.as_view(), name='buy-ticket'),

    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', Logout.as_view(), name='sign-out'),
    
    path('profile/<int:spec_id>/', ProfileSpectatorView.as_view(), name='profile'),
    path('profile/<int:spec_id>/wallet', WalletSpectatorView.as_view(), name='wallet'),
    path('purchase/', SpectatorPurchaseView.as_view(), name='purchase'),
]
