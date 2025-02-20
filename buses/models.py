from django.db import models
class Bus(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    running_days = models.JSONField()  # Example: ["Monday", "Wednesday", "Friday"]
    
    def __str__(self):
        return f"{self.name} - {self.total_seats} seats"
#stores bus details 
class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    
    def available_seats(self):
           booked = Booking.objects.filter(route=self).aggregate(Sum("booked_seats"))["booked_seats__sum"] or 0
           return self.bus.total_seats - booked
