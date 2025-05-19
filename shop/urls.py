from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop, name='shop'),
    path('orders/', views.order_history, name='order_history'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('modify_order/<int:order_id>/', views.modify_order, name='modify_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]