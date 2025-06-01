from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Review(models.Model):
    """
    Model for user reviews.
    Links `User` to a foreign key.
    Allows multiple reviews per user
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string of the review
        along with user name and star rating.
        """
        return (
            f"{self.user.first_name} {self.user.last_name} "
            f"- {self.rating}⭐"
        )
