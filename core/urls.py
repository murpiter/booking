from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = routers.DefaultRouter()
router.register(r"reservations", views.ReservationViewSet)

urlpatterns = [
    path("rooms/", views.RoomListAPIView.as_view(), name="api_rooms"),
    path("rooms/<int:pk>", views.RoomDetailAPIView.as_view(), name="api_rooms_detail"),
    path(
        "user/register/",
        views.UserRegisterAPIView.as_view(),
        name="api_user_register",
    ),
    path("user/obtain_token/", obtain_auth_token, name="api_obtain_token"),
]
