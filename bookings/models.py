from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError



# Create your models here.
class TeaPackage(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    tiers = models.IntegerField()
    sweet_options = models.IntegerField()
    savoury_options = models.IntegerField()
    includes_prosecco = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bookings', db_index=True)
    guest_name = models.CharField(max_length=100, blank=False, null=False, default="Unregistered Guest")
    guest_email = models.EmailField(blank=False, null=False, default="user@email.com")
    package = models.ForeignKey(TeaPackage, on_delete=models.CASCADE, default=1)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    guests_with_special_requests = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)

    def clean(self):
        super().clean()

        if self.date and self.date < now().date():
            raise ValidationError("Booking date cannot be in the past.")

        if self.date and self.time and self.date == now().date() and self.time < now().time():
            raise ValidationError("Booking time cannot be in the past.")

        if (self.guests_with_special_requests or 0) > self.number_of_guests:
            raise ValidationError("The number of guests with special requests cannot exceed the total number of guests.")
        
        if not self.customer and (not self.guest_name or not self.guest_email):
            raise ValidationError("Guest bookings require both a name and an email for confirmation.")


    def __str__(self):
        customer_name = self.customer.username if self.customer else self.guest_name
        return f"Booking for {customer_name} - {self.package.name} on {self.date} at {self.time}"

