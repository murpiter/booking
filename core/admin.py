from django.contrib import admin

from core.models import Reservation, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", "price")

    @admin.display(description="room")
    def title(self, obj):
        return f"{obj.number} ({obj.price})"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("room", "date_start", "date_end")

    @admin.display(description="room")
    def title(self, obj):
        return f"{obj.room.number} {obj.date_start} {obj.date_end}"
