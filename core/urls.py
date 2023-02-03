from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings


from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'room', views.RoomViewSet)
router.register(r'reservation', views.ReservationViewSet)


urlpatterns = [
    path('', views.RoomsView.as_view(), name='rooms'),
    path('authorize/', views.AuthorizeView.as_view(), name='authorize'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('room/<int:room_id>/', views.RoomDetailView.as_view(), name='room'),
    path('user_reservations/', views.UserReservationsView.as_view(), name='reservations'),
    path('api/', include(router.urls)),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
