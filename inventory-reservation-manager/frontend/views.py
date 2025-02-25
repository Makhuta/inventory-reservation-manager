from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime as DT
from django.http import JsonResponse, HttpResponse
import csv

from .functions import custom_render

from database.models import Item, Client, Reservation
from database.forms import ItemForm, ClientForm, ReservationForm, CSVUploadForm


# Create your views here.
@login_required
def index(request):
    return redirect('inventory')
    return custom_render(request, "index.html")

@login_required
def download(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'

    writer = csv.writer(response)

    # Add a header row
    writer.writerow(["Jméno Klient", "Telefon", "Email", "Jméno Item", "IČ", "Popis", "Od", "Do"])  # Adjust columns as needed

    # Add some sample data (optional, remove if not needed)
    for reservation in Reservation.objects.all():
        client = reservation.client
        item = reservation.item
        writer.writerow([client.name, client.phone, client.email, item.name, item.inventory_number, item.description, reservation.start, reservation.end])

    return response

@login_required
def my_logout(request):
    logout(request)
    return redirect('index')


# Inventory

@login_required
def inventory(request):
    items = Item.objects.all()
    return custom_render(request, "inventory/index.html", {'items': items })

@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("inventory")
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "inventory/add.html", {'form': ItemForm(request.POST), 'errors': e})
    return custom_render(request, "inventory/add.html", {'form': ItemForm(), 'errors': []})

@login_required
def item_modify(request):
    if request.method == 'POST':
        pk = request.GET.get("pk")
        if not pk:
            return redirect('inventory')
        form = ItemForm(request.POST, request.FILES, instance=Item.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return custom_render(request, "inventory/edit.html", {'form': ItemForm(instance=form.instance), 'errors': []})
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "inventory/edit.html", {'form': ItemForm(request.POST), 'errors': e})
    pk = request.GET.get("pk")
    if not pk:
        return redirect('inventory')
    item = Item.objects.get(pk=pk)
    return custom_render(request, "inventory/edit.html", {'form': ItemForm(instance=item), 'item': item, 'errors': []})

@login_required
def item_delete(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            Item.objects.get(pk=pk).delete()
            return redirect('inventory')
    pk = request.GET.get("pk")
    if not pk:
        return redirect('inventory')
    return custom_render(request, "inventory/delete.html", { 'item': Item.objects.get(pk=pk) })



# Reservations

@login_required
def reservations(request):
    rezerfations = Reservation.objects.all()
    return custom_render(request, "reservations/index.html", {'reservations': rezerfations})

@login_required
def reservations_add(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "reservations/add.html", {'form': ReservationForm(request.POST), 'errors': e})

    pk = request.GET.get("pk")
    initial = {}
    if pk:
        item = Item.objects.get(pk=pk)
        if item:
            initial['item'] = item
            last_rent = Reservation.objects.filter(item=pk).order_by('-end')
            if last_rent.exists():
                initial['start'] = last_rent.first().end
                initial['end'] = initial['start'] + DT.timedelta(days=7)
    

    return custom_render(request, "reservations/add.html", {'form': ReservationForm(initial=initial), 'errors': []})

@login_required
def reservations_return(request):
    if request.method == 'GET':
        pk = request.GET.get("pk")
        if pk:
            rezerfation = Reservation.objects.get(pk=pk)
            rezerfation.returned = not rezerfation.returned
            rezerfation.save()
    return redirect('reservations')


@login_required
def reservations_modify(request):
    if request.method == 'POST':
        pk = request.GET.get("pk")
        if not pk:
            return redirect('reservations')
        form = ReservationForm(request.POST, instance=Reservation.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return custom_render(request, "reservations/edit.html", {'form': ReservationForm(instance=form.instance), 'errors': []})
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "reservations/edit.html", {'form': ReservationForm(request.POST), 'errors': e})
    pk = request.GET.get("pk")
    if not pk:
        return redirect('reservations')
    reserv = Reservation.objects.get(pk=pk)
    return custom_render(request, "reservations/edit.html", {'form': ReservationForm(instance=reserv), 'reservation': reserv, 'errors': []})

@login_required
def reservations_delete(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            Reservation.objects.get(pk=pk).delete()
            return redirect('reservations')
    pk = request.GET.get("pk")
    if not pk:
        return redirect('reservations')
    return custom_render(request, "reservations/delete.html", { 'reservation': Reservation.objects.get(pk=pk) })



# Clients

@login_required
def clients(request):
    clients = Client.objects.all()
    return custom_render(request, "clients/index.html", {'clients': clients})

@login_required
def clients_add(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("clients")
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "clients/add.html", {'form': ClientForm(request.POST), 'errors': e})
    return custom_render(request, "clients/add.html", {'form': ClientForm(), 'errors': []})


def handle_uploaded_file(file):
    decoded_file = file.read().decode('utf-8')
    csv_data = csv.reader(decoded_file.splitlines(), delimiter=";")

    for (name, phone, email) in csv_data:
        if not name or not phone or not email:
            continue

        client = Client()
        client.name = name
        client.phone = phone
        client.email = email
        client.save()

@login_required
def clients_import(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['csv_file'])
            return redirect("clients")
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "clients/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': e})
    return custom_render(request, "clients/import.html", {'form': CSVUploadForm(), 'errors': []})

@login_required
def clients_modify(request):
    if request.method == 'POST':
        pk = request.GET.get("pk")
        if not pk:
            return redirect('clients')
        form = ClientForm(request.POST, instance=Client.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return custom_render(request, "clients/edit.html", {'form': ClientForm(instance=form.instance), 'errors': []})
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "clients/edit.html", {'form': ClientForm(request.POST), 'errors': e})
    pk = request.GET.get("pk")
    if not pk:
        return redirect('clients')
    client = Client.objects.get(pk=pk)
    return custom_render(request, "clients/edit.html", {'form': ClientForm(instance=client), 'client': client, 'errors': []})

@login_required
def clients_delete(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            Client.objects.get(pk=pk).delete()
            return redirect('clients')
    pk = request.GET.get("pk")
    if not pk:
        return redirect('clients')
    return custom_render(request, "clients/delete.html", { 'client': Client.objects.get(pk=pk) })