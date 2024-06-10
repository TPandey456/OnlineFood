from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.marketplace, name='marketplace'),

 
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    #add to cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),

    #decrease cart
    path('decrease_Cart/<int:food_id>/', views.decrease_Cart, name='decrease_Cart'),

    #delete the cart item
     path('delete_Cart/<int:cart_id>/', views.delete_Cart, name='delete_Cart'),





]
