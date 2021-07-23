from django.shortcuts import render, HttpResponse,  redirect
from .models import *
from restraunt.models import *
import uuid
from django.conf import UserSettingsHolder

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login , logout


def logout_attempt(request):
    logout(request)
    return redirect('/')

# Shokeeper Register and send mail
def shopkeeperRegister(request):
    try:
        if request.method == 'POST':
           
            email = request.POST.get('email')
            phone_number = request.POST.get('phonenumber')
            password = request.POST.get('password')
           
            if Shopkeeper.objects.filter(username = email).first():
               # messages.error(request, 'Email allready There')
                return  redirect('shopkeeperRegister')
            email_token = str(uuid.uuid4())
            Shopkeeper_obj = Shopkeeper.objects.create(username = email,email=email,phone_number=phone_number, email_token= email_token)
            Shopkeeper_obj.set_password(password)
            Shopkeeper_obj.save()
            sendmailregister(email, email_token)
            return redirect('/verifymsg')
            print('account created')
    except Exception as e:
           print(e)
    return render(request, 'Shopkeeper/register-shopkeeper.html')

# Shopkeeper Send Verificationa Email
def sendmailregister(username, email_token):
    try:
        subject = "Link to verify the your Account"
        message = f"Hi! here's the link to activate your account http://127.0.0.1:8000/accounts/shopkeeper/verifyshop{email_token}"
        email_from = settings.EMAIL_HOST_USER
     
        print("Email send initiated")
        send_mail(subject , message,email_from ,[username])
        print("Email has been Sent")
    except Exception as e:
        print(e)


def verifymsg(request):
    return render(request, 'Shopkeeper/verify.html')

# Shopkeeper Verify Email
def verify_Shopkeeper(request, email_token):
    try:
        Shopkeeper_obj = Shopkeeper.objects.get(email_token = email_token)
        Shopkeeper_obj.email_verified = True
        Shopkeeper_obj.save()
        return HttpResponse('Your account is verified')
    except Exception as e:
        print(e)
    return HttpResponse('Invalid Token')

# Shopkeeper Login
def shopkeeperlogins(request):

    if request.user.is_authenticated and  request.user.shopkeeper.is_authenticated:
        return redirect('/restaurant/Add_restraunt/')
 

    try:

        if request.user.is_authenticated and  request.user.shopkeeper.is_authenticated:
            return redirect('/restaurant/Add_restraunt/')
    except Exception as e:
        print(e)  

    try:
        if request.method == 'POST':
            email = request.POST.get('Loginemail')
            password = request.POST.get('loginpass')
            try:
                Shopkeeper_objlogin = Shopkeeper.objects.filter(username=email).first()
                print(Shopkeeper_objlogin)
                if Shopkeeper_objlogin is None:
                    return HttpResponse("Please register first")
                if not Shopkeeper_objlogin.email_verified:
                    return HttpResponse("Please verify your email first")
                 
                user=authenticate(username=email, password=password)
                print(user)
                if user is None:
                    print("user in non")
                    return HttpResponse('Incorrect')
                            
                login(request, user)
                print("user logined")
                try:
                    return redirect('/restaurant/Add_restraunt/')
                except Exception as e:
                    print(e)
               

            except Exception as e:
                print(e)    

    except Exception as e:
        print(e)    
    return render(request, 'Shopkeeper/login-shopkeeper.html')

# Shopkeeper forget Password
def forgetpassword(request):
    try:
        if request.method == 'POST':
            emails = request.POST.get('forgetpass')

            try:

                shopkeeper_forget= Shopkeeper.objects.filter(username=emails).first()
               
                print(shopkeeper_forget)
            
                if not shopkeeper_forget:
                    return HttpResponse("your email is not registered")
                
                user_obj = User.objects.get(username=emails)
                email_tokenss = str(uuid.uuid4())
                print(email_tokenss)
                shopkeeper_forget = Shopkeeper.objects.get(email = user_obj)
                shopkeeper_forget.forgetpass_token=email_tokenss
                print(shopkeeper_forget)
                shopkeeper_forget.save()
                forgetpassemail(emails, email_tokenss)
                
                return HttpResponse("The mail has been sent to your account")
            except Exception as e:
                print(e)         
    except Exception as e:
        print(e)        
    return render(request,'Shopkeeper/forgetpass-shopkeeper.html' )  

# Shopkeeper forget password send mail
def forgetpassemail(username, email_tokenss):
    try:
        subject = "Forget Passwor email"
        message = f"Hi! here's the link to reset your account http://127.0.0.1:8000/accounts/shopkeeper/newpassword-{email_tokenss}"
        email_from = settings.EMAIL_HOST_USER

        print("Email send initiated")
        send_mail(subject , message,email_from ,[username])
        print("Email has been Sent")
        
    except Exception as e:
        print(e)


# def verify_Shopkeeperforgetmail(request, email_tokens):
#     try:
#         Shopkeeper_obj = Shopkeeper.objects.get(forgetpass_token = email_tokens)
      
#         Shopkeeper_obj.save()
#         return redirect('newpassword')
#     except Exception as e:
#         print(e)
#     return HttpResponse('Invalid Token')

# Shopkeeper Set New Passsword and verify forget password token
def newpassword(request, email_tokenss):
    try:
        shopkeeper_objss = Shopkeeper.objects.get(forgetpass_token=email_tokenss)
        if request.method == 'POST':
            newpass = request.POST.get('newpassA')
            conferpass = request.POST.get('newpassB')
            if newpass != conferpass:
                return HttpResponse("password not same")
                
            shopkeeper_objss.set_password(conferpass)
            shopkeeper_objss.save()
                       
            return redirect('shopkeeperlogin')
            
    except Exception as e:
        print(e)
        
    return render(request, 'Shopkeeper/newpass-shopkeeper.html')

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#Here starts Customer views

def customerregister(request):
    try:
        if request.method == 'POST':
           
            email = request.POST.get('email')
            phone_number = request.POST.get('phonenumber')
            password = request.POST.get('password')
           
            if Customer.objects.filter(username = email).first():
               # messages.error(request, 'Email allready There')
                return  redirect('customerRegister')
            emailtoken = str(uuid.uuid4())
            customer_obj = Customer.objects.create(username = email,email = email,phonenumber=phone_number, emailtoken= emailtoken)
            customer_obj.set_password(password)
            customer_obj.save()
            sendmailregister_customer(email, emailtoken)
            return redirect('/verifycustomermsg')
            print('account created')


    except Exception as e:
        print(e)    
    return render(request, 'Customer/register-customer.html')

def verifymsg(request):
    return render(request, 'Customer/verify-customer.html') 


def sendmailregister_customer(username, emailtoken):
    try:
        subject = "Link to verify the your Account"
        message = f"Hi! here's the link to activate your account http://127.0.0.1:8000/accounts/shopkeeper/verifyshop{email_token}"
        email_from = settings.EMAIL_HOST_USER
     
        print("Email send initiated")
        send_mail(subject , message,email_from ,[username])
        print("Email has been Sent")
    except Exception as e:
        print(e)



def verify_customer(request, emailtoken):
    try:
        customer_obj = Customer.objects.get(emailtoken = email_token)
        customer_obj.emailverified = True
        customer_obj.save()
        return HttpResponse('Your account is verified')
    except Exception as e:
        print(e)
    return HttpResponse('Invalid Token')



# Customer Login
def customerlogin(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('Loginemail')
            password = request.POST.get('loginpass')
            try:
                customer_obj = Customer.objects.filter(username=email).first()
                print(customer_obj)
                if customer_obj is None:
                    return HttpResponse("Please register first")
                if not customer_obj.emailverified:
                    return HttpResponse("Please verify your email first")
                 
                user=authenticate(username=email, password=password)
                print(user)
                if user is None:
                    print("user in non")
                    return HttpResponse('Incorrect')
                            
                login(request, user)
                print("user logined")
                try:
                    return redirect('/')
                except Exception as e:
                    print(e)

               

            except Exception as e:
                print(e)    

    except Exception as e:
        print(e)    
    return render(request, 'Customer/login-customer.html')


#Customer Forget Password
def forgetpassword_customer(request):
    try:
        if request.method == 'POST':
            emails = request.POST.get('forgetpass')

            try:

                customer_forget= Customer.objects.filter(username=emails).first()
               
                print(customer_forget)
            
                if not customer_forget:
                    return HttpResponse("your email is not registered")
                
                user_obj = User.objects.get(username=emails)
                email_tokens = str(uuid.uuid4())
                print(email_tokens)
                customer_forget = Shopkeeper.objects.get(email = user_obj)
                customer_forget.customerpass_token=email_tokens
                print(customer_forget)
                customer_forget.save()
                forgetpassemail(emails, email_tokens)
                
                return HttpResponse("The mail has been sent to your account")
            except Exception as e:
                print(e)         
    except Exception as e:
        print(e)        
    return render(request,'Shopkeeper/forgetpass-shopkeeper.html' )      

# Shopkeeper forget password sen mail
def forgetpassemail_customer(username, email_tokens):
    try:
        subject = "Forget Passwor email"
        message = f"Hi! here's the link to reset your account http://127.0.0.1:8000/accounts/shopkeeper/verify_Shopkeeperforgetmail{email_tokens}"
        email_from = settings.EMAIL_HOST_USER

        print("Email send initiated")
        send_mail(subject , message,email_from ,[username])
        print("Email has been Sent")
        
    except Exception as e:
        print(e)