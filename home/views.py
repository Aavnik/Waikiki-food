from django.shortcuts import render, redirect
from restraunt.models import Restraunt
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    try:
        restoshop = Restraunt.objects.all()
        context = {'restraunts' : restoshop}
    except Exception as e:
        print(e)    
    return render(request , 'home/home.html', context)

def restraunt_detail(request , slug):
    try:
        restraunt_obj = Restraunt.objects.get(id = slug)
        context = {'restraunt' :restraunt_obj , 'menus' : restraunt_obj.restraunt.all()}
        return render(request , 'home/restro-details.html' , context)
    except Exception as e:
        print(e)

    return redirect('/error/')

def cartitems(request):
    return render(request , 'home/cart_items.html')
<<<<<<< HEAD
@login_required(login_url='/accounts/login/')
def success(request):

    
    return render(request , 'home/paysuccess.html')
@login_required(login_url='/accounts/login/')    
def fails(request):
    return render(request , 'home/payfails.html')
=======
>>>>>>> dc727c27638e92ac1ac0b447e5e20139a075f46e

