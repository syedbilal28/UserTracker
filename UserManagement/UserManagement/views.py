from django.shortcuts import render
from UserTracker.models import Website

def qrcode(request):
    name = "Welcome to"

    obj = Website.objects.get(id=1)

    context = {
        'name': name,
        'obj' : obj,
    }

    return render(request, 'qrcode.html', context)