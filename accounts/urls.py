from django.urls import path
from accounts.views import *
from . import views
from .views import *

urlpatterns = [

  path('shopkeeper/register/', views.shopkeeperRegister, name='shopkeeperRegister'),
  path('shopkeeper/login/', views.shopkeeperlogins, name='shopkeeperlogin'),
  path('shopkeeper/forgetpass/', views.forgetpassword, name='forgetpassword'),
  path('shopkeeper/newpassword-<email_tokenss>', views.newpassword, name='newpassword'),
  path('shopkeeper/verify', views.verifymsg, name = 'verifymsg'),
  path('shopkeeper/forgetmailsent', views.forgetpassemail, name = 'forgetpassemail'),
  path('shopkeeper/verifyshop<email_token>/', views.verify_Shopkeeper, name = 'verify_Shopkeeper'),
  #path('shopkeeper/verify_Shopkeeperforgetmail<email_tokens>/', views.verify_Shopkeeperforgetmail, name = 'verify_Shopkeeperforgetmail'),
 
  #-----------------------------------------------------------------------------------------------------------------------------------------
  path('register/', views.customerregister, name='customerregister'),
  path('login/', views.customerlogin, name='customerlogin'),
  path('forgetpassword/', views.forgetpassword_customer, name='forgetpassword_customer'),
  #path('shopkeeper/newpassword/', views.newpassword, name='newpassword'),
  path('verify', views.verifymsg, name = 'verifycustomermsg'),
  
  path('logout/' , views.logout_attempt , name="logut")

  #path('shopkeeper/verify<emailtoken>/', views.verify_customer, name = 'verify_customer'),
  #path('shopkeeper/verify_Shopkeeperforgetmail<email_tokens>/', views.verify_Shopkeeperforgetmail, name = 'verify_Shopkeeperforgetmail'),
]