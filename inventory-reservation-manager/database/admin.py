from django.contrib import admin

from .models import Client, Item, Reservation

# Register your models here.
admin.site.register(Client)
admin.site.register(Item)
admin.site.register(Reservation)