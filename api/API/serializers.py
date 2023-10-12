from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, DateField
from rest_framework.utils.serializer_helpers import ReturnDict

from cinema.models import Showtime, ScreenHall, Film
from cinema_admin.models import CinemaUser


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
    screen = CharField(source='screen.name')

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
    screen = CharField(source='screen.name')

    class Meta:
        model = Showtime
        exclude = ('price',)


class ScreenHallForAdminShowtimeContextSerializer(serializers.ModelSerializer):
    """
    Serializer for ScreenHall objects used in the context of the admin showtimes view.
    """
    amount_showtimes = IntegerField()

    class Meta:
        model = ScreenHall
        fields = ('name', 'amount_showtimes')


class AdminShowtimeContextSerializer(serializers.Serializer):
    """
    Serializer for representing additional context data used in the admin showtimes view.
    """
    selected_day = DateField()
    selected_screen = CharField()
    screens = ScreenHallForAdminShowtimeContextSerializer(many=True)
    amount_all_showtimes = IntegerField()


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
