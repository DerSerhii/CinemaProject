from django.contrib import admin

from .models import ScreenHall, Film, Showtime

admin.site.register(ScreenHall)
admin.site.register(Film)
admin.site.register(Showtime)
