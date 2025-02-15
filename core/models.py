from django.db import models
from django.contrib.auth.models import AbstractUser

class PASSENGER(AbstractUser): 
    admin = models.BooleanField(default=False) #Using it to differentiate between admin and passengers
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
class MAIN(models.Model): #For defining Database tables
    name = models.CharField(max_length=60)
    starting = models.CharField(max_length=60)
    destination = models.CharField(max_length=60)
    departure = models.DateTimeField()
    availability = models.IntegerField()

    def __str__(self): 
        return f"{self.name} ({self.starting} → {self.destination})"

class Booking_Model(models.Model): 
    user = models.ForeignKey(PASSENGER, on_delete=models.CASCADE)
    bus = models.ForeignKey(MAIN, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Booking by {self.user.username} for {self.bus.name}"
        