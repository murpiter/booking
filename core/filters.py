from django_filters.rest_framework import FilterSet, NumberFilter, DateFilter


from .models import Room


class RoomFilter(FilterSet):
    date_start = DateFilter(field_name="reservation__date_end", lookup_expr="gte", exclude=True)
    date_end = DateFilter(field_name="reservation__date_start", lookup_expr="lte", exclude=True)

    min_price = NumberFilter(field_name="price", lookup_expr="gt")
    max_price = NumberFilter(field_name="price", lookup_expr="lt")
    min_capacity = NumberFilter(field_name="capacity", lookup_expr="gt")
    max_capacity = NumberFilter(field_name="capacity", lookup_expr="lt")

    class Meta:
        model = Room
        fields = ["capacity", "price", "reservation__date_end", "reservation__date_start"]
