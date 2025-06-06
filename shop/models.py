from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from decimal import Decimal


# Selection Boxes
class SelectionBox(models.Model):
    """
    Model representing a selection box of various cakes.
    """
    box_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        """
        Returns a string of the box type and price
        """
        return f"{self.box_type} - €{self.price}"


# Individual Cakes
class Cake(models.Model):
    """
    Model representing an individual cake to buy.
    """
    cake_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        """
        Returns a string of the cake type and price
        """
        return f"{self.cake_type} - €{self.price}"


# Order Model
STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]


# Setting time now+1
def default_pickup_time():
    """
    Sets pickup time to 1 hour after order submitted.
    """
    return now() + timedelta(hours=1)


class Order(models.Model):
    """
    Model detailing a customer order.
    Links to `User` via foreign key.
    Relates to `OrderItem`
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(default=default_pickup_time)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    def save(self, *args, **kwargs):
        """
        Save the order instance and ensures pickup time is set
        """
        if not self.pk and not self.pickup_time:
            self.pickup_time = now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def update_total_price(self):
        """
        Calculates total price of the order.
        """
        self.total_price = sum(
            item.quantity * item.price
            for item in self.order_items.all()
        )
        self.save()

    def __str__(self):
        """
        Returns string of the order.
        Displays name and total price.
        """
        return (
            f"Order {self.id} by {self.user.first_name} "
            f"{self.user.last_name} - Total: €{self.total_price}"
        )


# Order Items Model
class OrderItem(models.Model):
    """
    Model that represents individual items in an order.
    Links to `Order` vis foreign key.
    Stores Cake or Box using `item_type` and `item_id`.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        null=True,
        blank=True,
    )
    item_type = models.CharField(
        max_length=10,
        choices=[
            ("cake", "Cake"),
            ("box", "Box"),
        ],
    )
    item_id = models.PositiveIntegerField()

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Returns string of order item.
        Displays item type, name and quantity
        """
        return f"{self.quantity}x {self.name} ({self.item_type})"

    def clean(self):
        """
        Calidates that each order item has type and name.
        """
        if not self.item_type or not self.name:
            raise ValidationError(
                "Order item must have a valid type and name."
            )

    def save(self, *args, **kwargs):
        """
        Saves order item after running checks.
        """
        self.clean()
        super().save(*args, **kwargs)
