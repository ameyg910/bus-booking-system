from django.urls import path
from .views import home, passenger_register, passenger_login, passenger_logout

urlpatterns = [
    path("", home, name="home"),  # ✅ Fix: Add home page route
    path("register/", passenger_register, name="passenger_register"),
    path("login/", passenger_login, name="passenger_login"),
    path("logout/", passenger_logout, name="passenger_logout"),
]
