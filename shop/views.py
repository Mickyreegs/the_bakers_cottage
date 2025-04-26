from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def my_shop(request):
    return HttpResponse("This is the shop section")