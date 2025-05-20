from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from decimal import Decimal

# Selection Boxes
class SelectionBox(models.Model):
    box_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.box_type} - €{self.price}"

# Individual Cakes
class Cake(models.Model):
    cake_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.cake_type} - €{self.price}"

# Order Model
STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(default=now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def save(self, *args, **kwargs):
        if not self.pickup_time or self.pickup_time.tzinfo is None:
            self.pickup_time = now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.first_name} {self.user.last_name} - Total: €{self.total_price}"

# Order Items Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, null=True, blank=True)
    box = models.ForeignKey(SelectionBox, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.cake or self.box}"

    def clean(self):
        if not self.cake and not self.box:
            raise ValidationError("Order item must contain a cake or a selection box.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
