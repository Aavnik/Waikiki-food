from django import urls
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from accounts.models import *
from restraunt.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import razorpay

client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

@login_required(login_url='/accounts/login/')
def add_cart(request , menu_id):
    try:
        customer = request.user.customer #got coustomer id
        cart_obj, _ =  Cart.objects.get_or_create(customer = customer , is_paid = False) # checked customer id and crate cart
        menu_obj = RestrauntMenu.objects.get(id = menu_id) # cheched menu id
        # now adding items inot cart using menu id
        if cart_obj.cart.filter(restraunt_menu = menu_obj).exists():
            cart_item_obj = CartItems.objects.get(cart = cart_obj,restraunt_menu = menu_obj)
                
            cart_item_obj.quantity += 1 
            cart_item_obj.save()
        else:
            CartItems.objects.create(cart = cart_obj,restraunt_menu =menu_obj )

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request , menu_id):
    try:
        customer = request.user.customer #got coustomer id
        cart_obj=  Cart.objects.get(customer = customer , is_paid = False) # checked customer id and crate cart
        menu_obj = RestrauntMenu.objects.get(id = menu_id)
        # now adding items inot cart using menu id
        if cart_obj.cart.filter(restraunt_menu = menu_obj).exists():
            cart_item_obj = CartItems.objects.get(cart = cart_obj,restraunt_menu = menu_obj)
            if cart_item_obj.quantity >0: 
                cart_item_obj.quantity -= 1 
                cart_item_obj.save()
                print(cart_item_obj)
            if cart_item_obj.quantity < 1:
                cart_obj_del = CartItems.objects.get(cart=cart_obj, restraunt_menu=menu_obj).delete()
            print("delete")

        else:
            pass
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required(login_url='/accounts/login/')
def cart_all_item_total(request):
    context ={}
    try:
        
        cust = request.user.customer
        cart_obj = Cart.objects.filter(customer=cust, is_paid=False).first()
        if cart_obj:
            print(cart_obj)
            carts_obj = CartItems.objects.filter(cart=cart_obj)
            print("item found")
            context["cart_obj"]=cart_obj 
            context["carts_obj"]=carts_obj
   
            # calculate total price of cart
            total_price =0
            for items in carts_obj:
                total_price += items.price
            cart_obj.total_price = total_price
            cart_obj.save() 
    except Exception as e:
        print(e)    

    return render(request , 'home/cart_items.html', context)


@login_required(login_url='/accounts/login/')
def checkout(request):
    try:
        customer = request.user.customer
        cart_obj = Cart.objects.get(customer= customer, is_paid=False)
        address_obj = CusomerAddress.objects.filter(customer=customer)
        print(Cart.total_price)
    
        if request.method =='POST':
            c_address = request.POST.get("address")
            c_state = request.POST.get("state")
            c_country = request.POST.get("country")
            c_pincode = request.POST.get("zip")
            add_address= CusomerAddress.objects.create(customer=customer,address=c_address,state=c_state,country=c_country,pincode=c_pincode)
            add_address.save()
        try:
            payment = client.order.create(
                {'amount':cart_obj.total_price*100,
                'currency' : 'INR' ,
                'payment_capture' :1}
            )
            cart_obj.razor_pay_order_id = payment['id']
            cart_obj.save()
        except Exception as e:
            print(e)
        return HttpResponse('Your cart is empty')
    except Exception as e:
        print(e)        
    return render(request, 'home/checkout.html',{'address_obj':address_obj,'cart_obj':cart_obj,'carts' : cart_obj , 'order_id':payment['id'] , 'key_id' : settings.KEY_ID})


# razorpay payment intigration
def payment_successfull(request):
    try:
        razor_pay_order_id = request.GET.get('razorpay_order_id')
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_signature = request.GET.get('razorpay_signature')   
        cart_obj = Cart.objects.get(razor_pay_order_id = razor_pay_order_id)
        cart_obj.is_paid = True
        cart_obj.razorpay_payment_id = razorpay_payment_id
        cart_obj.razorpay_signature = razorpay_signature
        cart_obj.save()
        
    except Exception as e:
        print(e)
    
    return render(request , 'home/paysuccess.html')
