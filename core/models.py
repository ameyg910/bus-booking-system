from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model for Passengers and Admins
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    # Fix conflicts with Django's auth system
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Unique related name
        blank=True
    )

# Bus Model
class Bus(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.source} → {self.destination})"

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.bus.name}"
