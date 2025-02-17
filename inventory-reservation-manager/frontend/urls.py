from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", views.my_logout, name="logout"),
    path("", views.index, name="index"),
    path("download", views.download, name="download"),


    path("inventory", views.inventory, name="inventory"),
    path("inventory/add", views.item_add, name="item_add"),
    path("inventory/modify", views.item_modify, name="item_modify"),
    path("inventory/delete", views.item_delete, name="item_delete"),


    path("reservations", views.reservations, name="reservations"),
    path("reservations/add", views.reservations_add, name="reservations_add"),
    path("reservations/modify", views.reservations_modify, name="reservations_modify"),
    path("reservations/delete", views.reservations_delete, name="reservations_delete"),


    path("clients", views.clients, name="clients"),
    path("clients/add", views.clients_add, name="clients_add"),
    path("clients/import", views.clients_import, name="clients_import"),
    path("clients/modify", views.clients_modify, name="clients_modify"),
    path("clients/delete", views.clients_delete, name="clients_delete"),
]
