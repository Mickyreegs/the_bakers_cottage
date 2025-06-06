from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form to submit user reviews.
    """
    class Meta:
        model = Review
        fields = ["comment", "rating"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your review...",
                }
            ),
            "rating": forms.Select(
                choices=[(i, f"{i} Stars") for i in range(1, 6)],
                attrs={"class": "form-control"},
            ),
        }
