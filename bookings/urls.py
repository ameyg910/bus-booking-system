from django.urls import path
from .views import book_ticket, user_bookings, cancel_booking

urlpatterns = [
     path("book/", book_ticket, name="book_ticket"),
    path("my-bookings/", user_bookings, name="user_bookings"),
    path("cancel/<int:booking_id>/", cancel_booking, name="cancel_booking"),
]
