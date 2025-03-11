from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now as date_now
from django.contrib.auth import logout
import datetime as DT
from django.http import JsonResponse, HttpResponse
import csv
from django.core.cache import cache
from django.template.defaulttags import register

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
    response['Content-Disposition'] = f'attachment; filename="inventory reservations view ({date_now().strftime("%d.%m.%Y %H:%M:%S")}).csv"'

    writer = csv.writer(response)

    writer.writerow(["Jméno Klient", "Telefon", "Email", "Jméno Item", "IČ", "Popis", "Od", "Do", "Vráceno"])

    for reservation in Reservation.objects.all():
        client = reservation.client
        item = reservation.item
        writer.writerow([client.name, client.phone, client.email, item.name, item.inventory_number, item.description, reservation.start, reservation.end, "Ano" if reservation.returned else "Ne"])

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
def items_import(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            decoded_file = file.read().decode('utf-8-sig')
            csv_data = list(csv.reader(decoded_file.splitlines(), delimiter=";"))

            if not csv_data:
                return custom_render(request, "inventory/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': ["Empty file"]})

            cache.set('uploaded_csv', csv_data, timeout=600)

            return custom_render(request, "inventory/preview.html", {
                'data': csv_data,
                'fields': [{'name': field.verbose_name, 'value': field.name} for field in Item._meta.local_fields if field.name != "image"]
            })
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "inventory/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': e})
    return custom_render(request, "inventory/import.html", {'form': CSVUploadForm(), 'errors': []})

@login_required
def items_confirm_import(request):
    if request.method == 'POST':
        csv_data = cache.get('uploaded_csv')
        if not csv_data:
            return redirect('items_import')

        remove_first_row = request.POST.get('remove_first_row', 'off') == 'on'
        if remove_first_row:
            csv_data = csv_data[1:]

        field_mapping = {str(i): request.POST.get(f"col_{i}") for i in range(len(csv_data[0]))}

        for row in csv_data:
            item_data = {}

            if 'id' in field_mapping.values():
                item_id_field_index = list(field_mapping.keys())[list(field_mapping.values()).index('id')]
                item_id = row[int(item_id_field_index)]

                try:
                    for index, model_field in field_mapping.items():
                        if model_field and model_field != 'id':
                            item_data[model_field] = row[int(index)]
                except Exception as e:
                    print(f"Error processing index {index}: {e}")

                try:
                    item, created = Item.objects.get_or_create(id=item_id, defaults=item_data)

                    if not created:
                        for model_field, value in item_data.items():
                            setattr(item, model_field, value)
                        item.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")
            else:
                try:
                    for index, model_field in field_mapping.items():
                        if model_field:
                            item_data[model_field] = row[int(index)]
                except Exception as e:
                    print(f"Error processing index {index}: {e}")

                try:
                    item = Item()
                    for model_field, value in item_data.items():
                        setattr(item, model_field, value)
                    item.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")

        cache.delete('uploaded_csv')
        return redirect("inventory")

    return redirect("items_import")

@login_required
def items_download(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="items ({date_now().strftime("%d.%m.%Y %H:%M:%S")}).csv"'

    writer = csv.writer(response, delimiter=";")

    fields = [{'name': field.verbose_name, 'value': field.name} for field in Item._meta.local_fields if field.name != "image"]


    writer.writerow([f.get("name") for f in fields])

    for item in Item.objects.all():
        writer.writerow([getattr(item, f["value"]) for f in fields])

    return response

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
def reservations_import(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            decoded_file = file.read().decode('utf-8-sig')
            csv_data = list(csv.reader(decoded_file.splitlines(), delimiter=";"))

            if not csv_data:
                return custom_render(request, "reservations/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': ["Empty file"]})

            cache.set('uploaded_csv', csv_data, timeout=600)

            return custom_render(request, "reservations/preview.html", {
                'data': csv_data,
                'fields': [{'name': field.verbose_name, 'value': field.name} for field in Reservation._meta.local_fields]
            })
        else:
            e = []
            for field, errors in form.errors.reservations():
                for error in errors:
                    e.append(error)
            return custom_render(request, "reservations/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': e})
    return custom_render(request, "reservations/import.html", {'form': CSVUploadForm(), 'errors': []})

@login_required
def reservations_confirm_import(request):
    if request.method == 'POST':
        csv_data = cache.get('uploaded_csv')
        if not csv_data:
            return redirect('reservations_import')

        remove_first_row = request.POST.get('remove_first_row', 'off') == 'on'
        if remove_first_row:
            csv_data = csv_data[1:]

        field_mapping = {str(i): request.POST.get(f"col_{i}") for i in range(len(csv_data[0]))}

        for row in csv_data:
            item_data = {}

            if 'id' in field_mapping.values():
                item_id_field_index = list(field_mapping.keys())[list(field_mapping.values()).index('id')]
                item_id = row[int(item_id_field_index)]

                for index, model_field in field_mapping.items():
                    try:
                        if model_field and model_field == 'item':
                            item = Item.objects.filter(id=row[int(index)])
                            if item.exists():
                                item_data[model_field] = item.first()
                        elif model_field and model_field == 'client':
                            client = Client.objects.filter(id=row[int(index)])
                            if client.exists():
                                item_data[model_field] = client.first()
                        elif model_field and model_field != 'id':
                            item_data[model_field] = row[int(index)]
                    except Exception as e:
                        print(f"Error processing index {index}: {e}")

                try:
                    item, created = Reservation.objects.get_or_create(id=item_id, defaults=item_data)

                    if not created:
                        for model_field, value in item_data.items():
                            setattr(item, model_field, value)
                        item.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")
            else:
                for index, model_field in field_mapping.items():
                    try:
                        if model_field and model_field == 'item':
                            item = Item.objects.filter(id=row[int(index)])
                            if item.exists():
                                item_data[model_field] = item.first()
                        elif model_field and model_field == 'client':
                            client = Client.objects.filter(id=row[int(index)])
                            if client.exists():
                                item_data[model_field] = client.first()
                        elif model_field and model_field != 'id':
                            item_data[model_field] = row[int(index)]
                    except Exception as e:
                        print(f"Error processing index {index}: {e}")

                try:
                    item = Reservation()

                    for model_field, value in item_data.items():
                        setattr(item, model_field, value)
                    item.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")

        cache.delete('uploaded_csv')
        return redirect("reservations")

    return redirect("reservations_import")


@login_required
def reservations_download(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="reservations ({date_now().strftime("%d.%m.%Y %H:%M:%S")}).csv"'

    writer = csv.writer(response, delimiter=";")

    fields = [{'name': field.verbose_name, 'value': field.name} for field in Reservation._meta.local_fields]


    writer.writerow([f.get("name") for f in fields])

    for reservation in Reservation.objects.all():
        writer.writerow([(getattr(reservation, f["value"]) if f["value"] not in ["item", "client"] else getattr(reservation, f["value"]).id) for f in fields])

    return response

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

@login_required
def clients_import(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            decoded_file = file.read().decode('utf-8-sig')
            csv_data = list(csv.reader(decoded_file.splitlines(), delimiter=";"))

            if not csv_data:
                return custom_render(request, "clients/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': ["Empty file"]})

            cache.set('uploaded_csv', csv_data, timeout=600)

            return custom_render(request, "clients/preview.html", {
                'data': csv_data,
                'fields': [{'name': field.verbose_name, 'value': field.name} for field in Client._meta.local_fields]
            })
        else:
            e = []
            for field, errors in form.errors.items():
                for error in errors:
                    e.append(error)
            return custom_render(request, "clients/import.html", {'form': CSVUploadForm(request.POST, request.FILES), 'errors': e})
    return custom_render(request, "clients/import.html", {'form': CSVUploadForm(), 'errors': []})

@login_required
def clients_confirm_import(request):
    if request.method == 'POST':
        csv_data = cache.get('uploaded_csv')
        if not csv_data:
            return redirect('clients_import')

        remove_first_row = request.POST.get('remove_first_row', 'off') == 'on'
        if remove_first_row:
            csv_data = csv_data[1:]

        field_mapping = {str(i): request.POST.get(f"col_{i}") for i in range(len(csv_data[0]))}

        for row in csv_data:
            client_data = {}

            if 'id' in field_mapping.values():
                client_id_field_index = list(field_mapping.keys())[list(field_mapping.values()).index('id')]
                client_id = row[int(client_id_field_index)].strip('\ufeff').strip()

                try:
                    for index, model_field in field_mapping.items():
                        if model_field and model_field != 'id':
                            client_data[model_field] = row[int(index)]
                except Exception as e:
                    print(f"Error processing index {index}: {e}")

                try:
                    client, created = Client.objects.get_or_create(id=client_id, defaults=client_data)

                    if not created:
                        for model_field, value in client_data.items():
                            setattr(client, model_field, value)
                        client.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")
            else:
                try:
                    for index, model_field in field_mapping.items():
                        if model_field:
                            client_data[model_field] = row[int(index)]
                except Exception as e:
                    print(f"Error processing index {index}: {e}")

                try:
                    client = Client()

                    for model_field, value in client_data.items():
                        setattr(client, model_field, value)
                    client.save()

                except Exception as e:
                    print(f"Error processing row {row}: {e}")

        cache.delete('uploaded_csv')
        return redirect("clients")

    return redirect("clients_import")

@login_required
def clients_download(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="clients ({date_now().strftime("%d.%m.%Y %H:%M:%S")}).csv"'

    writer = csv.writer(response, delimiter=";")

    fields = [{'name': field.verbose_name, 'value': field.name} for field in Client._meta.local_fields]


    writer.writerow([f.get("name") for f in fields])

    for client in Client.objects.all():
        writer.writerow([getattr(client, f["value"]) for f in fields])

    return response

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









@register.filter
def get_range(value):
    return range(value)