from rest_framework import serializers

from .models import Reservation, Room, User


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['room', 'user', 'date_start', 'date_end']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['price', 'capacity', 'number', 'id']
