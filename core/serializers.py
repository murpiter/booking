from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Reservation, Room


class UserRegistrationRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )

        Token.objects.create(user=user)

        return user


class UserRegistrationResponseSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')

    class Meta:
        model = User
        fields = ['username', 'email', 'token']



class UserAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'capacity', 'price', 'number']


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'capacity', 'price', 'number']


class ReservationCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ['room', 'date_start', 'date_end', 'user']


class ReservationListSerializer(serializers.ModelSerializer):
    room = RoomListSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'date_start', 'date_end', 'room']


class ReservationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id']
