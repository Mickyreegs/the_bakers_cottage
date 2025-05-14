from django.shortcuts import render, redirect, get_object_or_404
from .models import TeaPackage, Booking
from .forms import BookingForm
from django.contrib import messages

# Create your views here.
def bookings(request):
    packages = TeaPackage.objects.all()
    bookings = Booking.objects.filter(customer=request.user) if request.user.is_authenticated else Booking.objects.none()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.customer = request.user
            else:
                if not booking.guest_name or not booking.guest_email:
                    messages.error(request, "Guest bookings require both a name and an email.")
                    return render(request, "bookings/bookings.html", {"packages": packages, "bookings": bookings, "form": form})
                
            booking.save()

            messages.success(request, "Your booking was successful!  See you soon!")
            return redirect("bookings")
    else:
        form = BookingForm()
    
    return render(request, "bookings/bookings.html", {"packages": packages, "bookings": bookings, "form": form})

