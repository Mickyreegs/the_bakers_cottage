from django import forms
from django.utils.timezone import now
from .models import Booking
from datetime import datetime


class BookingForm(forms.ModelForm):
    """
    Form to handle Customer bookings
    """

    guest_name = forms.CharField(
        required=False,
        label="Guest Name (if not logged in)"
    )
    guest_email = forms.EmailField(
        required=False,
        label="Guest Email (if not logged in)"
    )
    time = forms.ChoiceField(
        choices=[
            (f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}")
            for h in range(11, 17)
            for m in [0, 15, 30, 45]
        ],
        required=True,
        label="Booking Time",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        """
        Initialises the booking form and
        auto-fills user details if authenticated
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            self.fields['guest_name'].initial = (
                self.user.get_full_name() or self.user.username
            )
            self.fields['guest_email'].initial = self.user.email
    # End of __init__



    class Meta:
        """
        Meta configuration for Booking form.
        Defines model associations, fields, labels,widgets.
        """
        model = Booking
        fields = [
            'guest_name',
            'guest_email',
            'package',
            'date',
            'time',
            'number_of_guests',
            'guests_with_special_requests',
            'special_requests'
            ]
        labels = {
            "number_of_guests": "Total Guests (Maximum 12)",
            "guests_with_special_requests": (
                "Number of guests with dietary needs"
            ),
            "special_requests": (
                "Special Dietary Requests / Event Requests e.g. Birthdays"
            ),
        }
        widgets = {
            'package': forms.Select(attrs={"class": "form-control"}),
            'date': forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "min": now().date(),
            }),
            'time': forms.Select(attrs={"class": "form-control"}),
            'number_of_guests': forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 12
            }),
            'guests_with_special_requests': forms.NumberInput(attrs={
                "class": "form-control",
            }),
            'special_requests': forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
        }

    def clean_date(self):
        """
        Validates that bookings cannot be in the past.
        """
        date = self.cleaned_data.get("date")
        if date < now().date():
            raise forms.ValidationError("You cannot select a past date.")
        return date

    def clean_time(self):
        """
        Validates that a booking cannot be for a time in the past
        """
        date = self.cleaned_data.get("date")
        time_string = self.cleaned_data.get("time")

        if date == now().date():
            try:
                time_obj = datetime.strptime(time_string, "%H:%M").time()
                if time_obj < now().time():
                    raise forms.ValidationError("You cannot select a time in the past.")
            except ValueError:
                raise forms.ValidationError("Invalid time format.")
        return time_string


    def clean(self):
        """
        Validates booking info for non-registered users
        and confirms Total guests !< special requests
        """
        cleaned_data = super().clean()
        guest_name = cleaned_data.get("guest_name")
        guest_email = cleaned_data.get("guest_email")
        special_request_guests = (
            cleaned_data.get("guests_with_special_requests") or 0)
        total_guests = cleaned_data.get("number_of_guests") or 1

        MAX_GUESTS = 12
        if total_guests > MAX_GUESTS:
            self.add_error(
                "number_of_guests",
                f"The number of guests that we can accommodate is {MAX_GUESTS} per booking."
            )

        user = getattr(self, 'user', None)
        if not user or not user.is_authenticated:
            if not guest_name:
                self.add_error("guest_name", "Guest bookings require a name.")
            if not guest_email:
                self.add_error("guest_email",
                               "Guest bookings require an email.")

        if special_request_guests > total_guests:
            self.add_error(
                "guests_with_special_requests",
                (
                    "The number of guests with special requests "
                    "cannot exceed the total number of guests."
                )
            )

        return cleaned_data
