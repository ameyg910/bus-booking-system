from django.db import models, transaction
from django.contrib.auth.decorators import login_required
@login_required
class Booking(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    bus = models.ForeignKey("buses.Bus", on_delete=models.CASCADE)
    route = models.ForeignKey("buses.Route", on_delete=models.CASCADE)
    booked_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_time = models.DateTimeField(auto_now_add=True)
    is_canceled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.bus.name} - {self.route}"
#handles ticket bookings 
class WalletTransaction(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[("credit", "Credit"), ("debit", "Debit")])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
#To track wallet balance usage. 
from django.utils.timezone import now, timedelta
@transaction.atomic
def cancel_booking(request, booking_id):
    user = request.user
    booking = get_object_or_404(Booking, id=booking_id, user=user, is_canceled=False)

    if not booking.can_cancel():
        return JsonResponse({"status": "error", "message": "Cannot cancel within 6 hours of departure."}, status=400)

    # Refund user
    user.wallet_balance += booking.total_price
    user.save()

    # Record refund transaction
    WalletTransaction.objects.create(user=user, amount=booking.total_price, transaction_type="credit")

    # Mark booking as canceled
    booking.is_canceled = True
    booking.save()

    return JsonResponse({"status": "success", "message": "Booking canceled and amount refunded."})
