from django import forms
from django.utils.timezone import now
from .models import Booking

class BookingForm(forms.ModelForm):
    guest_name = forms.CharField(required=False, label="Guest Name (if not logged in)")
    guest_email = forms.EmailField(required=False, label="Guest Email (if not logged in)")

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
        widgets = {
            'package': forms.Select(attrs={"class": "form-control"}),
            'date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'time': forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
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


    def clean_guests_with_special_requests(self):
        special_request_guests = self.cleaned_data.get("guests_with_special_requests", 0)
        total_guests = self.cleaned_data.get("number_of_guests", 1)

        if special_request_guests and special_request_guests > total_guests:
            raise forms.ValidationError("Number of guests with special requests cannot exceed the total number of guests.")
        
        return special_request_guests
    

    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get("guest_name")
        guest_email = cleaned_data.get("guest_email")
        customer = self.instance.customer

        if not customer and (not guest_name or not guest_email):
            raise forms.ValidationError("Guest bookings require both a name and an email.")
        
        return cleaned_data


