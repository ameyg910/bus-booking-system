from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_passenger = models.BooleanField(default=True) #identifies passenger accounts
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #stores users funds for booking
    
    def __str__(self):
        return self.username
