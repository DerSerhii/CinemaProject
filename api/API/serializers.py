from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueValidator

from cinema.models import Spectator, Showtime, ScreenCinema


class SpectatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      required=True)

    class Meta:
        model = Spectator
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'password2',
                  )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.\
                ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        customer = Spectator(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class ShowtimeViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = "__all__"


class ScreenCinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenCinema
        fields = "__all__"
