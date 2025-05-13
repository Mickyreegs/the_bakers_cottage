from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def update_booking_status(sender, instance, **kwargs):
    if instance.number_of_guests >= 6:
        instance.status = 'confirmed'
        instance.save()
