from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("rooms/", views.RoomListAPIView.as_view(), name="api_rooms"),
    path(
        "rooms/<int:pk>", views.RoomDetailAPIView.as_view(), name="api_rooms_detail"
    ),
    path(
        "reservations/",
        views.ReservationListAPIView.as_view(),
        name="api_reservations",
    ),
    path(
        "reservations/create/",
        views.ReservationCreateAPIView.as_view(),
        name="api_reservations_create",
    ),
    path(
        "reservations/<int:pk>/delete/",
        views.ReservationDeleteAPIView.as_view(),
        name="api_reservations_delete",
    ),
    path(
        "user/register/",
        views.UserRegisterAPIView.as_view(),
        name="api_user_register",
    ),
    path("user/obtain_token/", obtain_auth_token, name="api_obtain_token"),
]
