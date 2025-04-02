from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", views.my_logout, name="logout"),
    path("", views.index, name="index"),
    path("download", views.download, name="download"),


    path("inventory", views.inventory, name="inventory"),
    path("inventory/list", views.inventory_list, name="inventory_list"),
    path("inventory/add", views.item_add, name="item_add"),
    path("items/import", views.items_import, name="items_import"),
    path("items/confirm_import", views.items_confirm_import, name="items_confirm_import"),
    path("items/download", views.items_download, name="items_download"),
    path("inventory/modify", views.item_modify, name="item_modify"),
    path("inventory/delete", views.item_delete, name="item_delete"),


    path("reservations", views.reservations, name="reservations"),
    path("reservations/list", views.reservations_list, name="reservations_list"),
    path("reservations/add", views.reservations_add, name="reservations_add"),
    path("reservations/return", views.reservations_return, name="reservations_return"),
    path("reservations/import", views.reservations_import, name="reservations_import"),
    path("reservations/confirm_import", views.reservations_confirm_import, name="reservations_confirm_import"),
    path("reservations/download", views.reservations_download, name="reservations_download"),
    path("reservations/modify", views.reservations_modify, name="reservations_modify"),
    path("reservations/delete", views.reservations_delete, name="reservations_delete"),


    path("clients", views.clients, name="clients"),
    path("clients/list", views.clients_list, name="clients_list"),
    path("clients/add", views.clients_add, name="clients_add"),
    path("clients/import", views.clients_import, name="clients_import"),
    path("clients/confirm_import", views.clients_confirm_import, name="clients_confirm_import"),
    path("clients/download", views.clients_download, name="clients_download"),
    path("clients/modify", views.clients_modify, name="clients_modify"),
    path("clients/delete", views.clients_delete, name="clients_delete"),
]
