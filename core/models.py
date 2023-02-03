from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    price = models.IntegerField()
    capacity = models.IntegerField()
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return str(self.room.number)
