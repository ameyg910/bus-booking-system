from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Q
from .models import Route, Bus
from bookings.models import Booking
from django.utils.timezone import now

def search_buses(request):
    origin = request.GET.get("origin")
    destination = request.GET.get("destination")
    departure_date = request.GET.get("date")  # Expected format: YYYY-MM-DD

    if not (origin and destination and departure_date):
        return JsonResponse({"status": "error", "message": "Missing required parameters."}, status=400)

    # Convert departure date to a datetime object
    try:
        departure_date = now().strptime(departure_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"status": "error", "message": "Invalid date format."}, status=400)

    # Filter routes based on search criteria
    routes = Route.objects.filter(
        origin__iexact=origin,
        destination__iexact=destination,
        departure_time__date=departure_date
    ).select_related("bus")

    results = []
    for route in routes:
        booked_seats = Booking.objects.filter(route=route).aggregate(total_booked=Sum("booked_seats"))["total_booked"] or 0
        available_seats = route.bus.total_seats - booked_seats

        if available_seats > 0:  # Only show buses with available seats
            results.append({
                "bus_name": route.bus.name,
                "route": f"{route.origin} → {route.destination}",
                "departure_time": route.departure_time.strftime("%H:%M"),
                "available_seats": available_seats,
                "fare": float(route.bus.fare),
                "bus_id": route.bus.id
            })

    if not results:
        return JsonResponse({"status": "error", "message": "No buses available for the given search."}, status=404)

    return JsonResponse({"status": "success", "buses": results})
