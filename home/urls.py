from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-review/', views.submit_review, name='submit_review'),
]