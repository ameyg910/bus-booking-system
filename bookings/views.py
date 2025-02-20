from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Booking, WalletTransaction
from buses.models import Route, Bus
from users.models import CustomUser

@login_required
def user_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).select_related("route", "bus").order_by("-booking_time")

    data = [
        {
            "bus": booking.bus.name,
            "route": f"{booking.route.origin} → {booking.route.destination}",
            "departure": booking.route.departure_time.strftime("%H:%M"),
            "seats": booking.booked_seats,
            "total_price": float(booking.total_price),
            "booking_time": booking.booking_time.strftime("%Y-%m-%d %H:%M"),
        }
        for booking in bookings
    ]

    return JsonResponse({"bookings": data})

@transaction.atomic  # Ensures rollback if any step fails
def book_ticket(request):
    if request.method == "POST":
        user = request.user
        route_id = request.POST.get("route_id")
        num_seats = int(request.POST.get("num_seats"))

        # Get route and bus
        route = get_object_or_404(Route, id=route_id)
        bus = route.bus

        # Check seat availability
        booked_seats = Booking.objects.filter(route=route).aggregate(total_booked=models.Sum("booked_seats"))["total_booked"] or 0
        available_seats = bus.total_seats - booked_seats

        if num_seats > available_seats:
            return JsonResponse({"status": "error", "message": "Not enough available seats."}, status=400)

        # Calculate total price
        total_price = num_seats * bus.fare

        # Check wallet balance
        if user.wallet_balance < total_price:
            return JsonResponse({"status": "error", "message": "Insufficient wallet balance."}, status=400)

        # Deduct wallet balance
        user.wallet_balance -= total_price
        user.save()

        # Record wallet transaction
        WalletTransaction.objects.create(user=user, amount=total_price, transaction_type="debit")

        # Create booking record
        booking = Booking.objects.create(
            user=user,
            bus=bus,
            route=route,
            booked_seats=num_seats,
            total_price=total_price,
        )

        return JsonResponse({"status": "success", "message": "Booking confirmed!", "booking_id": booking.id})

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

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
