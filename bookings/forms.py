from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    guest_name = forms.CharField(required=False, label="Guest Name (if not logged in)")
    guest_email = forms.EmailField(required=False, label="Guest Email (if not logged in)")


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
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


    def clean_guests_with_special_requests(self):
        special_request_guests = self.cleaned_data.get("guests_with_special_requests", 0)
        total_guests = self.cleaned_data.get("number_of_guests", 1)

        if special_request_guests and special_request_guests > total_guests:
            raise forms.ValidationError("Number of guests with special requests cannot exceed the total number of guests.")
        
        return special_request_guests

