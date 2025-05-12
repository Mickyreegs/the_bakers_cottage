from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Selection boxes
class SelectionBox(models.Model):
    box_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.box_type} - €{self.price}"



#Individual cakes
class Cake(models.Model):
    cake_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.cake_type} - €{self.price}"
