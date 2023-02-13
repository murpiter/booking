from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("", views.RoomsView.as_view(), name="rooms"),
    path("authorize/", views.AuthorizeView.as_view(), name="authorize"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("room/<int:room_id>/", views.RoomDetailView.as_view(), name="room"),
    path(
        "user_reservations/", views.UserReservationsView.as_view(), name="reservations"
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        {"next_page": settings.LOGOUT_REDIRECT_URL},
        name="logout",
    ),
    path("api/rooms/", views.RoomListAPIView.as_view(), name="api_rooms"),
    path(
        "api/rooms/<int:pk>", views.RoomDetailAPIView.as_view(), name="api_rooms_detail"
    ),
    path(
        "api/reservations/",
        views.ReservationListAPIView.as_view(),
        name="api_reservations",
    ),
    path(
        "api/reservations/create/",
        views.ReservationCreateAPIView.as_view(),
        name="api_reservations_create",
    ),
    path(
        "api/reservations/<int:pk>/delete/",
        views.ReservationDeleteAPIView.as_view(),
        name="api_reservations_delete",
    ),
    path(
        "api/user/register/",
        views.UserRegisterAPIView.as_view(),
        name="api_user_register",
    ),
    path("api/user/obtain_token/", obtain_auth_token, name="api_obtain_token"),
]
