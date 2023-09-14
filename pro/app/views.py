from django.shortcuts import render,redirect
from .forms import SignUpForm,LoginForm,ChangePwd,PaymentForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

def home(req):
    return render(req,"app/base.html")

def Signup(req):
    if req.method=="POST":
        fm=SignUpForm(req.POST)
        if fm.is_valid():
            fm.save()
            messages.success(req,'Registered Successfully')
            SignUpForm()
    else:
        fm=SignUpForm()
    return render(req,"app/signup.html",{"fm":fm})
    
def Login(req):
    if req.method=="POST":
        fm=LoginForm(request=req,data=req.POST)
        if fm.is_valid():
            uname=fm.cleaned_data["username"]
            pwd=fm.cleaned_data["password"]
            user=authenticate(username=uname,password=pwd)
            if user is not None:
                login(req,user)
                messages.success(req,"Login Successfully")
    else:
        fm=LoginForm()
    return render(req,"app/login.html",{"fm":fm})

def Logout(req):
    logout(req)
    messages.success(req,"logged out successfully")
    fm=SignUpForm()
    return render(req,'app/signup.html',{'fm':fm})

def Changepwd(req):
    return render(req,"app/passwordchange.html")

def Men(req):
    data=Product.objects.filter(category='sh')
    data1=Product.objects.filter(category='te')
    return render(req,"app/all.html",{"data":data,"data1":data1})

def Women(req):
    data=Product.objects.filter(category='dt')
    data1=Product.objects.filter(category='je')
    data2=Product.objects.filter(category='ja')
    return render(req,"app/all.html",{"data":data,"data1":data1,"data2":data2})


def Dress(req):
    data=Product.objects.filter(category='dt')
    return render(req,"app/dress.html",{"data":data})
def Jeans(req):
    data=Product.objects.filter(category='je')
    return render(req,"app/dress.html",{"data":data})
def Jacket(req):
    data=Product.objects.filter(category='ja')
    return render(req,"app/dress.html",{"data":data})
def Shirt(req):
    data=Product.objects.filter(category='sh')
    return render(req,"app/dress.html",{"data":data})
def Tee(req):
    data=Product.objects.filter(category='te')
    return render(req,"app/dress.html",{"data":data})
def Sunglass(req):
    data=Product.objects.filter(category='su')
    return render(req,"app/dress.html",{"data":data})
def Watch(req):
    data=Product.objects.filter(category='wa')
    return render(req,"app/dress.html",{"data":data})
def Candle(req):
    data=Product.objects.filter(category='ca')
    return render(req,"app/dress.html",{"data":data})
       

def Search(req):
    if req.method=='POST':
        sear=req.POST['sear']
        s=Product.objects.filter(name__contains=sear)
        return render(req,"app/search.html",{'s':s})
    

def ProductDetail(req,id):
    pro= Product.objects.get(id=id)
    return render(req,"app/dressdetail.html",{"pro":pro})
    
def filterprice(req):
    if req.method=="POST" and req.POST.get('mx'):
        mx=int(req.POST.get('mx'))
        print(mx)
        mn=int(req.POST.get('mn'))
        print(mn)
        data=Product.products.get_product(mx,mn)
        print(data)
        return render(req,'app/filter.html',{'data':data})
    data=Product.objects.all()
    return render(req,'app/filter.html',{'data':data})

def AddToCart(req):
    user=req.user
    data=req.POST
    print(data.values())
    pro_id=req.GET.get("pro_id") 
    print(pro_id)   
    product=Product.objects.get(id=pro_id)  
    print(product)
    Cart(user=user, product=product).save()
    return redirect("/showcart/")

def ShowCart(req):
    if req.method=="POST" and req.POST.get('change'):
        ch=int(req.POST.get('change'))
        user=req.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        global totalamount
        shipping_charges=70.0
        totalamount=0.0
        # ids=int(req.POST.get("ids"))
        # cart1=Cart.objects.filter(id=ids)
        cart1=Cart.objects.all()
        # print(cart1.values())
        
        if cart1:
            for i in cart1:
                print(i.id)
                print(i.user_id)
                print(i.product_id)
                print(i.quantity)
                # amt=Product.objects.get(product_id=i.product_id)
                # print(i.product.discountedprice)
                tempamt=(ch*i.product.discountedprice)
                print(tempamt)
                tempamt = (ch*i.product.discountedprice)
                amount+=tempamt
                totalamount=amount+shipping_charges        
    else:    
        user=req.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_charges=70.0
        
        totalamount=0.0
        cart1=Cart.objects.all()        
        # print(cart1)
        if cart1:
            for i in cart1:
                tempamt=(i.product.discountedprice)
                amount+=tempamt
                totalamount=amount+shipping_charges
    return render(req,"app/cart.html",{"cart":cart,"totalamount":totalamount,"amount":amount})

def RemoveItems(req,id):
    c=Cart.objects.get(pk=id)
    c.delete()
    return redirect("/showcart/")


def item_payment(request):
    if request.method=="POST":
        name = request.POST['name']
        amount = int(totalamount) * 100
        client = razorpay.Client(auth=("rzp_test_kLdrKDm35HZ41B" , "3ppDS5oQwCpGYZPWOe2PhVG4" ))
        response_payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
    
        print(response_payment)
        order_status = response_payment['status']
        order_id = response_payment['id']
        
        if order_status=='created':
            product = ItemModel(name=name , amount =amount , order_id = response_payment['id'],)
            product.save()
            response_payment['name'] = name
            fm = PaymentForm( request.POST or None)
            print(fm)
            return render(request,'app/item_payment.html',{'form':fm,'payment':response_payment})

    fm = PaymentForm()
    return render(request,'app/item_payment.html',{'form':fm})

@csrf_exempt
def payment_status(request):
    # print(request.POST)
    if request.method=='POST':
        response = request.POST
        print(response)
        params_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth=("rzp_test_kLdrKDm35HZ41B" , "3ppDS5oQwCpGYZPWOe2PhVG4" ))

        try:
            status = client.utility.verify_payment_signature(params_dict)
            item = ItemModel.objects.get(order_id=response['razorpay_order_id'])
            item.razorpay_payment_id = response['razorpay_payment_id']
            item.paid = True
            item.save()
            return render(request, 'app/payment_status.html', {'status': True})
        except:
            return render(request, 'app/payment_status.html', {'status': False})
    return render(request, 'app/payment_status.html')

