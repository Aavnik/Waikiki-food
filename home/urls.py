from django.urls import path, include
from home.views import *
urlpatterns = [
    path('' , home),
    path('restraunt-details/<slug>/' , restraunt_detail , name="restraunt_detail"),
    path('cart-items/' , cartitems , name="cartitems"),
    path('success/' , success , name="success"),
    path('fails/' , fails , name="fails"),
   
]
