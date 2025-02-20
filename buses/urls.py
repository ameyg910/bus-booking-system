from django.urls import path
from .views import search_buses

urlpatterns = [
    path("search/", search_buses, name="search_buses"),
]
