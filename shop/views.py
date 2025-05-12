from django.shortcuts import render
from .models import SelectionBox, Cake
from django.http import HttpResponse

# Create your views here.

def shop(request):
    selection_boxes = SelectionBox.objects.all()

    cakes = Cake.objects.all()

    return render(request, "shop/shop.html", {"selection_boxes": selection_boxes, "cakes": cakes})




