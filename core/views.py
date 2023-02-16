from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
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


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True

        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReservationListSerializer
        elif self.request.method == "POST":
            return ReservationCreateSerializer
        elif self.request.method == "DELETE":
            return ReservationDeleteSerializer

        raise NotImplementedError()


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserRegistrationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = serializer.save()

        response_data = UserRegistrationResponseSerializer(new_user).data

        return Response(response_data, status=status.HTTP_201_CREATED)
