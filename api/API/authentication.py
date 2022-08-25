from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from diploma.settings import PERIOD_OF_INACTIVITY_BEFORE_LOGOUT


class TokenWithLifeTimeAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key=key)

        if (token.created + PERIOD_OF_INACTIVITY_BEFORE_LOGOUT) < timezone.now():
            token.delete()
            raise exceptions.AuthenticationFailed("Token expired")

        return user, token
