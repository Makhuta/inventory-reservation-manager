from django.db import models
import datetime as DT
from django.utils.timezone import now as date_now, timedelta as date_td
import hashlib
import os
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

# Create your models here.
def get_image_filename(instance, filename):
    file_hash = hashlib.md5(filename.encode()).hexdigest()
    file_extension = os.path.splitext(filename)[1]
    return f'images/{file_hash}{file_extension}'

def default_place_pics():
    return "static/default.png"

class Item(models.Model):
    name = models.CharField(max_length=64)
    inventory_number = models.CharField(max_length=32)
    image = models.ImageField(upload_to=get_image_filename, max_length=100, default=default_place_pics)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            if self.pk:
                old_image = Item.objects.get(pk=self.pk).image
                if old_image and old_image != self.image:
                    if default_storage.exists(old_image.path):
                        default_storage.delete(old_image.path)
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            if default_storage.exists(self.image.path):
                default_storage.delete(self.image.path)
        super().delete(*args, **kwargs)



class Client(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} ({self.email})'


class Reservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    start = models.DateField(default=date_now)
    end = models.DateField(default=(date_now() + date_td(days=7)))

    def __str__(self):
        return f'{self.item} - {self.client} ({self.start} -> {self.end})'
    

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('The start time must be before the end time.')
        
        overlapping_reservation = Reservation.objects.filter(
            item=self.item
        ).exclude(id=self.id).filter(
            start__lt=self.end,
            end__gt=self.start
        ).exists()

        if overlapping_reservation:
            raise ValidationError('There is already another reservation for this item in the specified time span.')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)