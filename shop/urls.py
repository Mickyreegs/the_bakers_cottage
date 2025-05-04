from . import views
from django.urls import path

urlpatterns = [
    path('', views.my_shop, name='shop'),    
]