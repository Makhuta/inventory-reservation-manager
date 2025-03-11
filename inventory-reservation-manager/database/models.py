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
    name = models.CharField(max_length=64, verbose_name="Name")
    inventory_number = models.CharField(max_length=32, verbose_name="IČ")
    image = models.ImageField(upload_to=get_image_filename, max_length=100, default=default_place_pics)
    description = models.CharField(max_length=1024, verbose_name="Description")

    @property
    def stocked(self):
        rezerfations = self.reservations.all()
        today_date = date_now().date()
        return all([r.returned for r in rezerfations if not(r.end > today_date and r.start > today_date)])
    
    def __str__(self):
        return self.name
    
    def is_default_image(self):
        return self.image.name == default_place_pics()

    def save(self, *args, **kwargs):
        if self.pk:
            item = Item.objects.filter(pk=self.pk).first()
            if item and item.image and item.image != self.image and not item.is_default_image():
                old_image_path = item.image.path
                if default_storage.exists(old_image_path):
                    default_storage.delete(old_image_path)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and not self.is_default_image():
            if default_storage.exists(self.image.path):
                default_storage.delete(self.image.path)
        super().delete(*args, **kwargs)

class Client(models.Model):
    name = models.CharField(max_length=64, verbose_name="Name")
    phone = models.CharField(max_length=32, verbose_name="Phone")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return f'{self.name} ({self.email})'

class Reservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations', verbose_name="Item ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations', verbose_name="Client ID")
    returned = models.BooleanField(default=False, verbose_name="Returned")
    start = models.DateField(default=date_now, verbose_name="Start date")
    end = models.DateField(default=(date_now() + date_td(days=7)), verbose_name="End date")

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