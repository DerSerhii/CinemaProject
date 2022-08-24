from django.contrib.auth import logout
from django.utils import timezone as tz
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

from diploma.settings import PERIOD_OF_INACTIVITY_BEFORE_LOGOUT


class LogoutWithoutUserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            last_activity = cache.get('last_request')
            if last_activity:
                if tz.now() > (last_activity + PERIOD_OF_INACTIVITY_BEFORE_LOGOUT):
                    logout(request)
            cache.set('last_request', tz.now())
