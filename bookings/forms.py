from django import forms
from django.utils.timezone import now
from .models import Booking

class BookingForm(forms.ModelForm):
    guest_name = forms.CharField(required=False, label="Guest Name (if not logged in)")
    guest_email = forms.EmailField(required=False, label="Guest Email (if not logged in)")
    time = forms.ChoiceField(
        choices=[(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(11, 17) for m in [0, 15, 30, 45]],  
        required=True,
        label="Booking Time",
        widget=forms.Select(attrs={"class": "form-control"})
    )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['guest_name'].initial = user.get_full_name() or user.username
            self.fields['guest_email'].initial = user.email


    class Meta:
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
            "number_of_guests": "Total Guests",
            "guests_with_special_requests": "Number of guests with dietary needs",
            "special_requests": "Special Dietary Requests / Event Requests e.g. Birthdays",
        }
        widgets = {
            'package': forms.Select(attrs={"class": "form-control"}),
            'date': forms.DateInput(attrs={"type": "date", "class": "form-control", "min": now().date()}),
            'time': forms.Select(attrs={"class": "form-control"}),
            'number_of_guests': forms.NumberInput(attrs={"class": "form-control"}),
            'guests_with_special_requests': forms.NumberInput(attrs={"class": "form-control"}),
            'special_requests': forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date < now().date():
            raise forms.ValidationError("You cannot select a past date.")
        return date
    

    def clean_time(self):
        date = self.cleaned_data.get("date")
        time = self.cleaned_data.get("time")

        if date == now().date() and time < now().time():
            raise forms.ValidationError("You cannot select a past time.")
        return time
    

    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get("guest_name")
        guest_email = cleaned_data.get("guest_email")
        customer = self.instance.customer
        special_request_guests = cleaned_data.get("guests_with_special_requests") or 0
        total_guests = cleaned_data.get("number_of_guests") or 1

        if not customer:
            if not guest_name:
                self.add_error("guest_name", "Guest bookings require a name.")
            if not guest_email:
                self.add_error("guest_email", "Guest bookings require an email.")

        if special_request_guests > total_guests:
            self.add_error(
                "guests_with_special_requests",
                "The number of guests with special requests cannot exceed the total number of guests."
            )


        return cleaned_data




