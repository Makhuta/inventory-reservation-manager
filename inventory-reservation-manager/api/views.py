from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime as DT

from database.models import Item, Client, Reservation

# Create your views here.

@login_required
def item_reservations(request):
    pk = request.GET.get("pk")
    if not pk:
        return JsonResponse({'reserved': []})
    
    rezerfations = Item.objects.get(pk=pk).reservations.values_list('client', 'start', 'end')
    reserved_dates = []
    reserved_clients = {}
    for client, start, end in rezerfations:
        current_date = start
        while current_date < end:
            d = current_date.strftime('%Y-%m-%d')
            reserved_dates.append(d)
            current_date += DT.timedelta(days=1)
            reserved_clients[d] = f'{Client.objects.get(pk=client)}'

    return JsonResponse({'reserved': reserved_dates, 'clients': reserved_clients})


@login_required
def reservation(request):
    pk = request.GET.get("pk")
    if not pk:
        return JsonResponse({'dates': []})
    
    rezerfations = Reservation.objects.get(pk=pk)
    reserved_dates = []
    current_date = rezerfations.start
    while current_date < rezerfations.end:
        d = current_date.strftime('%Y-%m-%d')
        reserved_dates.append(d)
        current_date += DT.timedelta(days=1)

    return JsonResponse({'dates': reserved_dates})