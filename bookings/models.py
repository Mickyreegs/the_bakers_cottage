from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.customer.username} on {self.date} at {self.time}"