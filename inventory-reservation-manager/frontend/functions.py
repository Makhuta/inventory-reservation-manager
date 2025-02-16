from django.shortcuts import render, redirect
from datetime import date

def custom_render(request, template_name, context={}):
    default_context = {
        'year': date.today().strftime("%Y"),
        'base_url': f'{request.scheme}://{request.get_host()}',
    }

    context.update(default_context)
    return render(request, template_name, context)