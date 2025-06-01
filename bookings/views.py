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
    bookings = (
        Booking.objects.select_related("package")
        .filter(customer=request.user)
        if request.user.is_authenticated
        else Booking.objects.none()
    )
    form = BookingForm(user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = (
                request.user if request.user.is_authenticated else None
            )

            try:
                booking.save()
                messages.success(
                    request,
                    "Your booking was successful! See you soon!"
                )
                return redirect(reverse("bookings"))
            except ValidationError as e:
                for field, error_list in e.error_dict.items():
                    for error in error_list:
                        form.add_error(field, error)

    return render(
        request,
        "bookings/bookings.html",
        {
            "packages": packages,
            "bookings": bookings,
            "form": form,
        }
    )
