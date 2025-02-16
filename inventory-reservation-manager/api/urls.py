from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("item_reservations", views.item_reservations, name="api_item_reservations"),
    path("reservation", views.reservation, name="api_reservation"),
]
