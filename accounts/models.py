from django.db import models
from django.contrib.auth.models import User
from home.models import BaseModel
# Shopkeeper , Customer 


class Shopkeeper(User):
    '''
    Shopkeeper model handling restraunt owner

    '''
    username = None
   # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    phone_number = models.CharField(max_length=10)
    email_token = models.CharField(max_length=100, null=True,blank=True)
    email_verified = models.BooleanField(default=False)
    forgetpass_token = models.CharField(max_length=100, null=True,blank=True)
    adhar_card = models.CharField(max_length=16)
    gst_number = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,
                choices=(('Male' , 'Male'),
                ('Female' , 'Female')))

    USERNAME_FIELD = 'email'
    class Meta:
        db_table = 'shopkeeper'



class Customer(User):
    phonenumber = models.CharField(max_length=10)
    emailtoken = models.CharField(max_length=100, null=True,blank=True)
    emailverified = models.BooleanField(default=False)
    customerpass_token = models.CharField(max_length=100, null=True,blank=True)


    def get_cart_count(self):
        try:
            cart = self.customer_cart.get(is_paid = False)
            return cart.cart.count()
        except Exception as e:
            return 0
        return 0


class CusomerAddress(BaseModel):
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    address = models.CharField(max_length=500,null= True, blank= True)
    country = models.CharField(max_length= 100, null= True, blank= False)
    state = models.CharField(max_length= 100, null= True, blank= True)
    pincode = models.CharField(max_length=100, null= True, blank= True)







