from django.shortcuts import render, redirect, get_object_or_404
from .models import TeaPackage, Booking
from .forms import BookingForm
from django.http import HttpResponse

# Create your views here.
def bookings(request):
    packages = TeaPackage.objects.all()
    bookings = Booking.objects.all()

    return render(request, "bookings/bookings.html", {"packages": packages, "bookings": bookings})
