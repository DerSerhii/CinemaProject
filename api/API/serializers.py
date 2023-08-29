from django.contrib.auth.password_validation import validate_password
from django.utils import timezone as tz
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueValidator

from cinema.models import Showtime, ScreenHall, Film
from cinema_admin.models import CinemaUser


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


class ShowtimeSerializers(serializers.ModelSerializer):
    film = serializers.CharField(source="film.name", read_only=True)
    screen = serializers.CharField(source="screen.name", read_only=True)

    class Meta:
        model = Showtime
        fields = "__all__"


class ShowtimeStaffSerializers(serializers.ModelSerializer):
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    class Meta:
        model = Showtime
        fields = ['date_start', 'date_end', 'time_start', 'film', 'screen', 'price']

    def validate(self, data):
        screen = data['screen']
        film = data['film']
        date_start = data.get('date_start',
                              tz.localtime().date())  # obj: datatime.date
        date_end = data['date_end']  # obj: datatime.date
        time_start = data['time_start']  # obj: datatime.time

        # check Start date
        if date_start < tz.localtime(tz.now()).date():
            raise serializers.ValidationError(
                {'date_start': 'Unable to create a showtime in the past'}
            )

        # check End date
        if date_start > date_end:
            raise serializers.ValidationError(
                {'date_end': "End date can't be less than Start date"}
            )

        # avoid creating sessions crossed by hall same date same time
        showtime = Showtime.objects.filter(screen=screen)
        if self.instance:
            showtime = showtime.exclude(pk=self.instance.pk)

        for sht in showtime:
            cross_days = (sht.start_date <= date_start <= sht.end_date) \
                         or (sht.start_date <= date_end <= sht.end_date)
            cross_hours = (sht.start_time <= time_start <= sht.time_end) \
                          or (sht.start_time <= time_end <= sht.time_end)
            if cross_days and cross_hours:
                raise serializers.ValidationError(
                    f"Session crosses at least with session id#{sht.pk}"
                )

        return data


class ScreenCinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenHall
        fields = "__all__"


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'
