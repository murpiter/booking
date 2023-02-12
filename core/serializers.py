from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Reservation, Room


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )


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
    room = RoomListSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'date_start', 'date_end', 'room']


class ReservationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id']
