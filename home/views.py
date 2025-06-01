from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.contrib import messages


# Create your views here.
def grouped_reviews(reviews, size=3):
    return [reviews[i:i + size] for i in range(0, len(reviews), size)]


def home(request):
    all_images = [
        "birthday-1.jpg",
        "display-1.jpg",
        "display-2.jpg",
        "display-3.jpg",
        "display-4.jpg",
        "display-5.jpg",
        "display-6.jpg",
        "display-7.jpg",
        "display-8.jpg",
        "hearts.jpg",
        "pastries.jpg",
        "raspberry.jpg",
        "wedding-cake-1.jpg",
        "wedding-cake-2.jpg",
        "wedding-cake-3.jpg"
    ]

    reviews = Review.objects.order_by("-created_at")
    user_reviews = grouped_reviews(reviews)
    form = ReviewForm()

    return render(request, "home/index.html", {
        "all_images": all_images,
        "reviews": user_reviews,
        "form": form,
    })


@login_required
def submit_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect("home")

    return redirect("home")
