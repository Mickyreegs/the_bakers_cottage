from django.shortcuts import render
from django.conf import settings

# Create your views here.

def contact(request):
    return render(request, "contact/contact.html", {"MAPS_KEY": settings.MAPS_KEY, "MAP_ID": settings.MAP_ID})
