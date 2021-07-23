from django.urls import path, include
from .views import *
urlpatterns = [
    path('add-cart/<menu_id>/' , add_cart  , name="add_cart"),
    path('remove-cart/<menu_id>/' , remove_cart  , name="remove_cart"),
    path('cart-items/' , cart_all_item_total  , name="cart_all_item_total"),
    path('checkout/' , checkout  , name="checkout"),
    path('payment-successfull/' , payment_successfull , name="payment_successfull")
   
]