from django.contrib import admin
from bookings.models import Booking, WalletTransaction

admin.site.register(Booking)
admin.site.register(WalletTransaction)
