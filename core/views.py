from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class IsAvailableFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_s = request.GET.get("date_start")

        date_e = request.GET.get("date_end")

        if date_s and date_e:
            rooms_id_to_exclude = Reservation.objects.filter(
                Q(date_start__gte=date_s, date_start__lte=date_e)
                | Q(date_end__gte=date_s, date_end__lte=date_e)
                | Q(date_start__lte=date_s, date_end__gte=date_e)
            ).values_list("room_id", flat=True)

            return queryset.exclude(id__in=rooms_id_to_exclude)

        return queryset


class RoomFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gt")
    max_price = NumberFilter(field_name="price", lookup_expr="lt")
    min_capacity = NumberFilter(field_name="capacity", lookup_expr="gt")
    max_capacity = NumberFilter(field_name="capacity", lookup_expr="lt")

    class Meta:
        model = Room
        fields = ["capacity", "price"]


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
    queryset = Reservation.objects.all()

    serializer_class = ReservationListSerializer


class ReservationCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    serializer_class = ReservationCreateSerializer


class ReservationDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    serializer_class = ReservationDeleteSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()

    serializer_class = UserRegistrationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = serializer.save()

        response_data = UserRegistrationResponseSerializer(new_user).data

        return Response(response_data, status=status.HTTP_201_CREATED)


class RoomsView(View):
    def get(self, request):
        sort = request.GET.get("sort", "price")

        date_s = request.GET.get("date_start")

        date_e = request.GET.get("date_end")

        if date_s and date_e:
            rooms_id_to_exclude = Reservation.objects.filter(
                Q(date_start__gte=date_s, date_start__lte=date_e)
                | Q(date_end__gte=date_s, date_end__lte=date_e)
                | Q(date_start__lte=date_s, date_end__gte=date_e)
            ).values_list("room_id", flat=True)

            rooms = Room.objects.exclude(id__in=rooms_id_to_exclude)

        else:
            rooms = Room.objects.all().order_by(sort)

        context = {
            "rooms": rooms,
        }

        return render(request, "core/rooms.html", context=context)


class AuthorizeView(View):
    def get(self, request):
        return render(request, "core/authorize.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Неправильно введён логин или пароль")
            return redirect("authorize")

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("rooms")


class RegisterView(View):
    def get(self, request):
        return render(request, "core/register.html")

    def post(self, request):
        if not request.user.is_anonymous:
            return redirect("rooms")

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(username, email, password)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        return redirect("rooms")


class RoomDetailView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        context = {
            "room": room,
        }
        return render(request, "core/room.html", context)

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)

        if request.user.is_anonymous:
            return redirect("authorize")

        date_start = request.POST["date_start"]
        date_end = request.POST["date_end"]

        Reservation.objects.create(
            room=room, user=request.user, date_start=date_start, date_end=date_end
        )

        context = {
            "room": room,
        }
        return render(request, "core/room.html", context)


class UserReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        context = {
            "reservations": reservations,
        }
        return render(request, "core/user_reservations.html", context)

    def post(self, request):
        Reservation.objects.filter(id=request.POST["reservation_id"]).delete()

        reservations = Reservation.objects.filter(user=request.user)
        context = {
            "reservations": reservations,
        }

        if reservations:
            return render(request, "core/user_reservations.html", context)

        else:
            return redirect("rooms")
