from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

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
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TeaPackage, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking for {self.customer.username} - {self.package.name} on {self.date} at {self.time}"
