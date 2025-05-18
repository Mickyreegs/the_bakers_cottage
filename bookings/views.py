from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import TeaPackage, Booking
from .forms import BookingForm

# Create your views here.
def bookings(request):
    packages = TeaPackage.objects.all()
    bookings = Booking.objects.select_related("package").filter(customer=request.user) if request.user.is_authenticated else Booking.objects.none()
    form = BookingForm(user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.customer = request.user
            else:
                if not booking.guest_name or not booking.guest_email:
                    messages.error(request, "Guest bookings require both a name and an email.")
                    return render(request, "bookings/bookings.html", {"packages": packages, "bookings": bookings, "form": form})    
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Your booking was successful! See you soon!")
                return redirect(reverse("bookings"))
            except ValidationError as e:
                messages.error(request, "; ".join(e.messages))
        else:
            form = BookingForm(user=request.user)

    return render(request, "bookings/bookings.html", {"packages": packages, "bookings": bookings, "form": form})