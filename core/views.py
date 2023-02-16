from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.filters import IsAvailableFilterBackend, RoomFilter
from core.models import Reservation, Room
from core.serializers import (
    ReservationCreateSerializer,
    ReservationDeleteSerializer,
    ReservationListSerializer,
    RoomDetailSerializer,
    RoomListSerializer,
    UserRegistrationRequestSerializer,
    UserRegistrationResponseSerializer,
)


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()

    serializer_class = RoomListSerializer

    filter_backends = [
        filters.OrderingFilter,
        IsAvailableFilterBackend,
        DjangoFilterBackend,
    ]
    filterset_class = RoomFilter
    ordering_fields = ["price", "capacity"]
    ordering = ["price"]


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()

    serializer_class = RoomDetailSerializer


class ReservationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.filter(is_deleted=False)

    serializer_class = ReservationListSerializer


class ReservationCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    serializer_class = ReservationCreateSerializer


class ReservationDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    serializer_class = ReservationDeleteSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True

        instance.save()


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserRegistrationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = serializer.save()

        response_data = UserRegistrationResponseSerializer(new_user).data

        return Response(response_data, status=status.HTTP_201_CREATED)
