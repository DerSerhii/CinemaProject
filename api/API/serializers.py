import datetime as dt

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.validators import UniqueForYearValidator

import utils
from cinema.models import Showtime, ScreenHall, Film
from cinema_admin.models import CinemaUser
from django.middleware.security import SecurityMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import CommonMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.middleware.clickjacking import XFrameOptionsMiddleware

class FilmSerializer(serializers.ModelSerializer):
    """
    Serializer for the Film model.
    """

    class Meta:
        model = Film
        fields = '__all__'


class ShowtimeForCinemaHomepageSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying showtime details on the Cinema Homepage API.
    """
    screen = serializers.CharField(source='screen.name')

    class Meta:
        model = Showtime
        fields = ('screen', 'start')


class CinemaShowtimeSerializer(serializers.Serializer):
    """
    Serializer for Cinema Homepage API to display films and their showtimes.
    """
    film = serializers.SerializerMethodField()
    showtime_today = serializers.SerializerMethodField()

    def get_film(self, obj) -> ReturnDict:
        """
        Custom method to retrieve and serialize film information.
        """
        return FilmSerializer(obj[0]).data

    def get_showtime_today(self, obj) -> ReturnDict:
        """
        Custom method to retrieve and serialize showtimes for the film.
        """
        return ShowtimeForCinemaHomepageSerializer(obj[1], many=True).data


class FilmForAdminShowtimeSerializer(serializers.ModelSerializer):
    """
    Serializer for Film objects used in the admin panel for Showtime.
    """

    class Meta:
        model = Film
        fields = ('title', 'duration', 'poster')


class ScreenHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenHall
        fields = '__all__'


class AdminShowtimeSerializer(serializers.ModelSerializer):
    """
    Serializer for Showtime objects used in the custom admin panel.
    """
    film = FilmForAdminShowtimeSerializer()
    screen = serializers.CharField(source='screen.name')

    class Meta:
        model = Showtime
        exclude = ('price',)


class ScreenHallForAdminShowtimeContextSerializer(serializers.ModelSerializer):
    """
    Serializer for ScreenHall objects used in the context of the admin showtimes view.
    """
    amount_showtimes = serializers.IntegerField()

    class Meta:
        model = ScreenHall
        fields = ('name', 'amount_showtimes')


class AdminShowtimeContextSerializer(serializers.Serializer):
    """
    Serializer for representing additional context data used in the admin showtimes view.
    """
    selected_day = serializers.DateField()
    selected_screen = serializers.CharField()
    screens = ScreenHallForAdminShowtimeContextSerializer(many=True)
    amount_all_showtimes = serializers.IntegerField()


class FilmDistributionCreationSerializer(serializers.Serializer):
    film = serializers.PrimaryKeyRelatedField(queryset=Film.objects.filter(is_active=True))
    release_day = serializers.DateField()
    last_day = serializers.DateField()
    start_hour = serializers.IntegerField()
    start_minute = serializers.IntegerField()
    screen = serializers.PrimaryKeyRelatedField(queryset=ScreenHall.objects.all())
    price = serializers.DecimalField(max_digits=5, decimal_places=2, max_value=1000, min_value=0)

    def validate(self, data) -> dict | None:
        """
        # Hook for doing extra form-wide cleaning.
        #
        # If the last day of distribution film is earlier than the release day,
        # then an error will be added to the field `last_day`.
        #
        # If the start of showtime is less than the current moment,
        # then ah error will be added to the filed `start_minute`.
        #
        # If film distribution that is being created has intersections
        # with existing showtimes, an error will be raised.
        """
        validator = utils.FilmDistributionCreationValidator(data)
        return validator.data

    def create(self, validated_data):
        film: Film = validated_data['film']
        release_day: dt.date = validated_data['release_day']
        last_day: dt.date = validated_data['last_day']
        start_datetime: dt.datetime = validated_data['start_datetime']
        screen: ScreenHall = validated_data['screen']
        price = validated_data['price']

        bulk_showtime = []
        for day in range((last_day - release_day).days + 1):
            start = start_datetime + dt.timedelta(days=day)
            end = start + film.duration
            bulk_showtime.append(
                Showtime(film=film, start=start, end=end, screen=screen, price=price)
            )
        return Showtime.objects.bulk_create(bulk_showtime)


class SpectatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      required=True)

    class Meta:
        model = CinemaUser
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'password2',
                  )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers. \
                ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        customer = CinemaUser(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer
