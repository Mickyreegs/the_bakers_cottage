from django.shortcuts import render
from django.conf import settings


# Create your views here.
def contact(request):
    """
    Handles the rendering of the contac page.
    Pulls keys from .env
    """
    return render(request, "contact/contact.html", {
        "MAPS_KEY": settings.MAPS_KEY,
        "MAP_ID": settings.MAP_ID,
        "EMAILJS_PUBLIC_KEY": settings.EMAILJS_PUBLIC_KEY
    })
