from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
import random
import requests
from datetime import *
from . models import *

def index(request):

    return render(request,'index.html')

def upicture(request):

    user = User.objects.get(email=request.session['email'])
    uprofile = UserProfile.objects.get(user=user)

    try:

        if request.method == "POST":

            if 'profile' in request.FILES:

                uprofile.profile = request.FILES['profile']
                uprofile.save()
                
                request.session['profile'] = uprofile.profile.url

                messages.success(request, "Picture Updated Successfully..!!")
            else:
            
                messages.error(request, "No picture selected..!!")

            return redirect('uprofile')
        
        else:
            return render(request, 'uprofile.html', {'uprofile': uprofile})
    
    except Exception as e:
        print(e)
        messages.error(request, "Picture Not Updated..!!")
        return redirect('uprofile')



def uprofile(request):

    user = User.objects.get(email=request.session['email'])
    uprofile = UserProfile.objects.get(user=user)
    
    if request.method == "POST":

        try:
            
            user.name = request.POST['name']
            user.mobile = request.POST['mobile']
            uprofile.uname = request.POST['uname']
            uprofile.address = request.POST['address']
            uprofile.gender = request.POST['gender']
            dob_str = request.POST['dob']
            
            if dob_str:
                uprofile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
            user.save() 
            uprofile.save()
            messages.success(request,"Profile Updated Successfully..!!")
            return redirect('uprofile') 
            
        except Exception as e:

            print(e)
            messages.error(request, "Profile Not Updated..!!")
            return redirect('uprofile') 
        
    else:

        if uprofile.dob:
         uprofile.dob = uprofile.dob.strftime('%Y-%m-%d')
                                              
        context = {
            'user': user,
            'uprofile': uprofile
        }
    
        if user.usertype == "customer":
            return render(request,'uprofile.html',context)
        else:
            return render(request,'seller/sprofile.html',context)
    

def signup(request):
    
    if request.method=="POST":

        try:
            user = User.objects.get(email=request.POST['email'])
            f_msg = "Email already exists...!!"
            return render(request,'signup.html',{'f_msg':f_msg})
        
        except:

            if request.POST['password'] == request.POST['cpassword']:

                user = User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    password = request.POST['password'],
                    usertype = request.POST['usertype']
                )

                UserProfile.objects.create(
                    user = user,
                    uname = request.POST['uname'],
                    profile = request.FILES['profile'],
                )

                s_msg = "Registration successfull..!! login here..!!"
                return render(request,'login.html',{'s_msg':s_msg})
            
            else:

                f_msg = "Password and Confirm Password does not match...!!"
                return render(request,'signup.html',{'f_msg':f_msg})
    else:

        return render(request,'signup.html')
    

def login(request):
    
    if request.method=="POST":
        
        try:

            user = User.objects.get(email=request.POST['email'])
            uprofile = UserProfile.objects.get(user=user)

            if user.password == request.POST['password']:

                request.session['email'] = user.email
                request.session['uname'] = uprofile.uname
                request.session['profile'] = uprofile.profile.url
                
                if user.usertype == "seller":
                    #messages.success(request,f'Welcome {user.name} !!')
                    return render(request,'seller/sindex.html')
                
                else:
                    #messages.success(request,f'Welcome {user.name} !!')
                    return render(request,'index.html')
                
            
            else:

                f_msg = "Password does not match.!!"
                return render(request,'login.html',{'f_msg':f_msg})

        except Exception as e:

            print(e)
            f_msg = "Email does not exist..!!"
            return render(request,'login.html',{'f_msg':f_msg})
    else:
        
        return render(request,'login.html')

def logout(request):

    del request.session['email']
    del request.session['profile']
    del request.session['uname']

    return redirect('login')


def cpass(request):

    user = User.objects.get(email=request.session['email'])

    if request.method == "POST":

        try:

            if user.password == request.POST['opass']:

                if request.POST['npass'] == request.POST['cnpass']:

                    user.password = request.POST['npass']
                    user.save()

                    return redirect(logout)
                
                else:

                    f_msg = "New password and Confirm New Password are not same..!!"

                    if user.usertype == "customer":
                        return render(request,'cpass.html',{'f_msg':f_msg})
                    else:
                        return render(request,'seller/scpass.html',{'f_msg':f_msg})

            else:

                f_msg = "Current password is wrong..!!"

                if user.usertype == "customer":
                    return render(request,'cpass.html',{'f_msg':f_msg})
                else:
                    return render(request,'seller/scpass.html',{'f_msg':f_msg})

        except:

            f_msg = "Password not changed try again..!!"

            if user.usertype == "customer":
                return render(request,'cpass.html',{'f_msg':f_msg})
            else:
                return render(request,'seller/scpass.html',{'f_msg':f_msg})
    else:

       if user.usertype == "customer":
            return render(request,'cpass.html')
       else:
            return render(request,'seller/scpass.html')

def fpass(request):

    if request.method == "POST":

        try:

            user = User.objects.get(mobile=request.POST['mobile'])
            mobile = request.POST['mobile']

            otp = random.randint(1001,9999)
                    
            url = "https://www.fast2sms.com/dev/voice"

            querystring = {"authorization":"qih0aQb3DLQ0Q6rQfxYDb0HnnQw2Flq54KwF08m9fXS5VUNuZm8jZIl1F1we","variables_values":otp,"route":"otp","numbers":int(mobile)}
            
            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)

            request.session['mobile'] = mobile
            request.session['otp'] = otp

            s_msg = "Verification code has been sent to your mobile..!!"
            return render(request,'fpass.html',{'s_msg':s_msg})
        
        except:

            f_msg = "Mobile number does not exists..!!"
            return render(request,'fpass.html',{'f_msg':f_msg})

    else:

        return render(request,'fpass.html')


def otp(request):

    otp = int(request.session['otp'])
    uotp = int(request.POST['uotp'])

    try:

        if otp == uotp:

            del request.session['otp']
            return render(request,'newpass.html')
        else:
            
            f_msg = "Invalid OTP, Try Again..!!"
            return render(request,'fpass.html',{'f_msg':f_msg})

    except:
        
        return render(request,'fpass.html')

def newpass(request):

    if request.method == "POST":

        try:

            user = User.objects.get(mobile=request.session['mobile'])

            if request.POST['npass'] == request.POST['cnpass']:

                user.password = request.POST['npass']
                user.save()

                del request.session['mobile']
                return redirect('login')

            else:

                f_msg = "New Password and Confirm New Password are not same..!!"
                return render(request,'newpass.html',{'f_msg':f_msg})

        except:

            f_msg = "Password not updated try again..!!"
            return render(request,'newpass.html',{'f_msg':f_msg})

    else:
    
        return render(request,'newpass.html')
    

def shop(request):
    product = Product.objects.all()
    mywish = []

    if request.session.get('email'):
        user = User.objects.get(email=request.session['email'])
        mywish = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)

    context = {
        'product': product,
        'mywish': mywish,
    }
   
    return render(request, 'shop.html', context)

def mdetails(request,pk):

    if request.session.get('email'):
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)
        mywish = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)
        mycart = Cart.objects.filter(user=user,payment=False).values_list('product_id', flat=True)

        context = {
            'product':product,
            'mywish':mywish,
            'mycart':mycart,
        }
        return render(request,'mdetails.html',context)

    else:

        messages.warning(request,'Please signup or login to view more details..!!')
        return redirect('shop')


def addwish(request, pk):
    
    if request.session.get('email'):
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)
        mycart = Cart.objects.filter(user=user, product=product)
        
        if mycart.exists():
            messages.info(request, 'Product already in your cart..!!')

            source = request.GET.get('source','shop')

            if source == 'shop':
                return redirect('shop')
            else:
                return redirect('mdetails',pk=pk)
        else:
            Wishlist.objects.create(user=user, product=product)
            
        source = request.GET.get('source','shop')

        if source == 'mdetails':
            messages.success(request, 'Product saved in your wishlist..!!')
            return redirect('mdetails',pk=pk)
        else:
            messages.success(request, 'Product added to your wishlist..!!')
            return redirect('shop')
    else:

        messages.warning(request,'Please signup or login to access wishlist..!!')
        return redirect('shop')


def removewish(request, pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    mywish = Wishlist.objects.filter(user=user, product=product)

    if mywish.exists():
        mywish.delete()  
    
    source = request.GET.get('source','shop')

    if source == 'wishlist':
        messages.warning(request, 'Product removed successfully..!!')
        return redirect('wishlist')
    elif source == 'mdetails':
        messages.warning(request, 'Product removed from wishlist..!!')
        return redirect('mdetails',pk=pk)
    else:
        messages.warning(request, 'Product removed from wishlist..!!')
        return redirect('shop')

def wishlist(request):

    user = User.objects.get(email=request.session['email'])
    mywish = Wishlist.objects.filter(user=user)

    return render(request, 'wishlist.html', {'mywish': mywish})

def cart(request):

    try:
        user = User.objects.get(email=request.session['email'])
        mycart = Cart.objects.filter(user=user)
        cttl = sum(item.pttl for item in mycart)

        return render(request,'cart.html',{'mycart':mycart,'cttl':cttl})
    
    except:
        return render(request,'cart.html')

def thankyou(request):

    return render(request,'thankyou.html')

def checkout(request):

    user = User.objects.get(email=request.session['email'])
    mycart = Cart.objects.filter(user=user)
    cttl = sum(item.pttl for item in mycart)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({'amount': cttl * 100, 'currency': 'INR', 'payment_capture': 1})

    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        razorpay_payment_id = request.POST.get('razorpay_payment_id')

        billing = BillingDetails.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state
        )

        order = Order.objects.create(
            user=user,
            billing=billing,
            total=cttl
        )

        for item in mycart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.pqty,
                price=item.product.pprice
            )
            item.payment = True
            item.save()

        # Clear the cart
        mycart.delete()

        return redirect('thankyou')

    context = {
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    }

    return render(request, 'checkout.html', {'mycart': mycart, 'cttl': cttl, 'context': context})

def myorders(request):
    user = User.objects.get(email=request.session['email'])
    orders = Order.objects.filter(user=user)
    return render(request, 'myorders.html', {'orders': orders})

def updateqty(request,pk):
    if request.method == "POST":
        cart = Cart.objects.get(pk=pk)
        cart.pqty = int(request.POST['pqty'])
        cart.pttl = cart.product.pprice * cart.pqty
        cart.save()
        return redirect('cart')
    return redirect('cart')

def addcart(request,pk):

    if request.session.get('email'):
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)

        mycart = Cart.objects.filter(user=user,product=product)

        if mycart.exists():
            
            source = request.GET.get('source','mdetails')

            if source == 'buynow':
                return redirect('cart')
            elif source == 'shop':
                messages.warning(request,'Product alreday in your cart..!!')
                return redirect('shop')
            else:
                messages.warning(request,'Product alreday in your cart..!!')
                return redirect('mdetails',pk=pk)

        else:
            Cart.objects.create(user=user,product=product,pqty=1,
                                pttl=product.pprice,cttl=product.pprice,
                                payment = False,)

            mywish = Wishlist.objects.filter(user=user,product=product)

            if mywish.exists():
                mywish.delete()

        source = request.GET.get('source','mdetails')
        
        if source == 'buynow':
            return redirect('cart')
        elif source == 'wishlist':
            messages.success(request,'Product added to your cart..!!')
            return redirect('wishlist')
        else:
            messages.success(request,'Product added to your cart..!!')
            return redirect('mdetails',pk=pk)
    else:
        messages.warning(request,'Please signup or login to buy products..!!')
        return redirect('shop')

def deletecart(request,pk):

    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    mycart = Cart.objects.filter(user=user,product=product)

    if mycart.exists():
        mycart.delete()

    source = request.GET.get('source','cart')

    if source == 'mdetails':
        messages.warning(request,'Product deleted from cart..!!')
        return redirect('mdetails',pk=pk)
    else:
        messages.warning(request,'Product deleted from cart..!!')
        return redirect('cart')   
    
    
def about(request):

    return render(request,'about.html')

def services(request):

    return render(request,'services.html')

def blog(request):

    return render(request,'blog.html')

def contact(request):

    return render(request,'contact.html')

#-----------------Seller Views------------------#

def sindex(request):

    return render(request,'seller/sindex.html')

def sprofile(request):

    return render(request,'seller/sprofile.html')

def plist(request):

    return render(request,'seller/plist.html')

def pdetails(request):

    return render(request,'seller/pdetails.html')

def padd(request):

    if request.method == "POST":
        seller = User.objects.get(email=request.session['email'],usertype='seller')
        try:    
            pname = request.POST['pname']
            pdesc = request.POST['pdesc']
            pprice = request.POST['pprice']
            pcat = request.POST['pcat']
            pimg = request.FILES['pimg']

            product = Product.objects.create(seller=seller,pname=pname, pdesc=pdesc, pprice=pprice, pcat=pcat, pimg=pimg)
            product.save()

            messages.success(request, "Product added successfully..!!")
            return redirect('padd')
        
        except Exception as e:
            print(e)
            return redirect('padd')
    else:

        return render(request,'seller/padd.html')

def pview(request):
    
    seller = User.objects.get(email=request.session['email'],usertype='seller')
    product = Product.objects.filter(seller=seller)
    return render(request,'seller/pview.html',{'product':product})

def pupdate(request,pk):

    seller = User.objects.get(email=request.session['email'],usertype='seller')
    product = Product.objects.get(pk=pk)

    if request.method == "POST":

        try:

            product.pname = request.POST['pname']
            product.pdesc = request.POST['pdesc']
            product.pprice = request.POST['pprice']
            product.pcat = request.POST['pcat']

            if 'pimg' in request.FILES:
                product.pimg = request.FILES['pimg']
            
            product.save()

            messages.success(request,'Product Updated Successfully..!!')
            return redirect('pview')

        except Exception as e:

            print(e)
            messages.error(request,'Product not updated, Please try again..!!')
            return redirect('pupdate',pk=pk)

    else:

        return render(request,'seller/pupdate.html',{'product':product})
    
def pdelete(request,pk):

    seller = User.objects.get(email=request.session['email'],usertype='seller')
    product = Product.objects.get(pk=pk)

    product.delete()
    messages.success(request,'Product Deleted Successfully..!!')
    return redirect('pview')