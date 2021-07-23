from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
from django.contrib.auth import logout


# Shopkeeper create restro here
@login_required(login_url='/accounts/shopkeeper/login/')
def Restraunt_add(request):
    restraunt_obj = Restraunt.objects.filter(shopkeeper = request.user.shopkeeper).first()
    if restraunt_obj:
        return redirect(f'/restaurant/selleradmin/{restraunt_obj.id}') 

    context = {}

    if request.method == 'POST':
        
        restraunts_name = request.POST.get("Restraunts_name")
        restraunt_descripton = request.POST.get("Restraunt_Desc")
        restraunt_address = request.POST.get("Restraunt_Adddress")
        restraunt_pincode = request.POST.get("Restraunt_pincode")
        restraunt_image = request.FILES.get("Restraunt_image")
        lattitude = request.POST.get("Restraunt_lattitude")
        longitude = request.POST.get("Restraunt_longitude")

        restraunt_obj = Restraunt.objects.create(
            shopkeeper = request.user.shopkeeper,
            restraunt_name=restraunts_name,
            restraunt_descripton=restraunt_descripton,
            restraunt_address=restraunt_address,
            restraunt_pincode=restraunt_pincode,
            restraunt_image=restraunt_image,
            lattitude=lattitude,
            longitude=longitude
        )
        return redirect(f'/restaurant/selleradmin/{restraunt_obj.id}') 
     
    return render(request, 'Restraunt/add_restraunt.html' , context)


#Shopkeeper  Add fooditems

@login_required(login_url='/accounts/shopkeeper/login/')
def selleradmins(request, restraunt_id):
    
    FoodItem_obj = FoodItem.objects.all()
    rest_obj = Restraunt.objects.get(id = restraunt_id)
    if rest_obj.shopkeeper != request.user.shopkeeper:
        return HttpResponse('You are authorized')
    print(rest_obj)
       
      
    if request.method == 'POST':
        
            
        data = request.POST
        food_name = request.POST.get("Food_name")
        food_price = request.POST.get("Food_price")
        food_description = request.POST.get("Food_Desc")
        food_catogery = request.POST.get("Food_type")
        food_image = request.FILES.get("Food_image")

       
        if data['Food_category']!='none':
            fooditem = FoodItem.objects.get(id=data['Food_category']) 
          
        resturant_item_obj= RestrauntMenu.objects.create(
            restraunt = rest_obj,
            menu_name = food_name,
            menu_price = food_price,
            menu_description = food_description,
            menu_type = food_catogery,
            food_item_type = fooditem,
            menu_image = food_image

            )
        resturant_item_obj.save()
    context = {'foodstype':FoodItem_obj, 'restraunt_id':restraunt_id}
    print(context)
    return render(request,'Restraunt/shopadmin.html', context)

# All food items display here
<<<<<<< HEAD
@login_required(login_url='/accounts/shopkeeper/login/')
def displayproduct(request):
    shopkeeper = request.user.shopkeeper
    display_obj = Restraunt.objects.get(shopkeeper=shopkeeper)
    del_obj = RestrauntMenu.objects.filter(restraunt=display_obj)
    print(display_obj.id)
    
    context ={'items':del_obj,'display_obj':display_obj}
=======

def displayproduct(request):
    display_obj = RestrauntMenu.objects.all()
    
    context ={'items':display_obj}
>>>>>>> dc727c27638e92ac1ac0b447e5e20139a075f46e

    return render(request,'Restraunt/displayproducts.html', context)


# food items delete here 

def deleteitem(request, del_id):
    delete_obj = RestrauntMenu.objects.get(id=del_id)
    if delete_obj.restraunt.shopkeeper != request.user.shopkeeper:
        return HttpResponse ("you are not authorised to delete this item")
    
    delete_obj.delete()
    context ={"del_id":del_id}
<<<<<<< HEAD
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'),context)
   # return render('Restraunt/displayproducts.html', context)
=======

    return render('Restraunt/displayproducts.html', context)
>>>>>>> dc727c27638e92ac1ac0b447e5e20139a075f46e

# shopkeeper Edit food items here

@login_required(login_url='/accounts/shopkeeper/login/')
def edititem(request, item_id):
    foodstype = FoodItem.objects.all()
    item_obj = RestrauntMenu.objects.get(id = item_id)

    if item_obj.restraunt.shopkeeper != request.user.shopkeeper:
        return HttpResponse('You are authorized')

    
    if request.method == 'POST':
        food_name = request.POST.get("Foodname")
        food_price = request.POST.get("Foodprice")
        food_description = request.POST.get("FoodDesc")
        food_catogery = request.POST.get("Foodtype")
<<<<<<< HEAD
        food_images = request.FILES.get('Foodimagess')
=======
        food_images = request.FILES.get("Foodimagess")
>>>>>>> dc727c27638e92ac1ac0b447e5e20139a075f46e
       
       
        RestrauntMenu.objects.filter(id = item_id).update( menu_name = food_name,
            menu_price = food_price,
            menu_description = food_description,
            menu_type = food_catogery,
           
            menu_image = food_images,
           
            )
       
        print(RestrauntMenu.menu_image)
             
    context = {'item_obj':item_obj ,'foodstype' :foodstype} 
    print(context)
    
        

    return render(request,'Restraunt/edit_items.html', context)

  #http://127.0.0.1:8000/restaurant/selleradmin/24f9980a-1e7a-440d-8648-4af89dd1a29b/ 

def all_orders(request):
    

    return render(request,'Restraunt/all_orders.html')
def shopdetail(request):
    shopkeeper = request.user.shopkeeper
    display_obj = Restraunt.objects.get(shopkeeper=shopkeeper)



    return render(request,'Restraunt/shopdetails.html',{'display_obj':display_obj})

        
        


    
   

