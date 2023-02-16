from django.db.models import Q
from django_filters.rest_framework import FilterSet, NumberFilter
from rest_framework import filters

from .models import Reservation, Room


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
