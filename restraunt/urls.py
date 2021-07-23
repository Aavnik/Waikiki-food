from django.urls import path
from restraunt.views import *
from . import views
from .views import *

urlpatterns = [

  path('Add_restraunt/', views.Restraunt_add, name='Restraunt_add'),
<<<<<<< HEAD
  path('all-order/', views.all_orders, name='all_orders'),
  path('shopdetail/', views.shopdetail, name='shopdetail'),
=======
>>>>>>> dc727c27638e92ac1ac0b447e5e20139a075f46e
  path('display-product/', views.displayproduct, name='displayproduct'),
  path('edit-item/<item_id>/', views.edititem, name='edititem'),
  path('delete-item/<del_id>/', views.deleteitem, name='deleteitem'),
  path('selleradmin/<restraunt_id>/', views.selleradmins, name='selleradmins'),



]