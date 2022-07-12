from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegisterationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitems = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        context={
            "topwears":topwears,
            "bottomwears":bottomwears,
            "mobiles":mobiles,
            "totalitems":totalitems,
        }
        return render(request,'app/home.html',context)

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitems = 0
        flag=False
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
            flag=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'flag':flag,"totalitems":totalitems})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id) 
    Cart(user=user,product=product).save() 
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        #print(cart_product)
        if cart_product:
            totalitems = 0
            totalitems = len(Cart.objects.filter(user=request.user))
            for p in cart_product:
                temp = (p.quantity)*(p.product.discounted)
                amount+=temp
            total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':carts,'amount':amount,'total_amount':total_amount,'shipping_amount':shipping_amount,"totalitems":totalitems})
        else:
            return render(request,'app/addtocart.html',{'nodata':"OOPS!! Nothing to show in cart..."})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))[0]
        c.quantity+=1
        c.save()
        print(c)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp = (p.quantity)*(p.product.discounted)
            amount+=temp  
        total_amount = amount+shipping_amount  
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount,
        }
    return JsonResponse(data)
        
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))[0]
        c.quantity-=1
        c.save()
        print(c)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp = (p.quantity)*(p.product.discounted)
            amount+=temp
        total_amount = amount+shipping_amount     
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount,
        }
    return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))[0]
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp = (p.quantity)*(p.product.discounted)
            amount+=temp
        total_amount = amount+shipping_amount     
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount,
        }
    return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op  = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data=='below':
        mobiles = Product.objects.filter(category='M').filter(discounted__lt=10000)
    elif data=='above':
        mobiles = Product.objects.filter(category='M').filter(discounted__gt=10000)
    else:
        #also try to filter by price
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html',{"mobiles":mobiles})



class CustomerRegisterationView(View):
    def get(self,request):
        form = CustomerRegisterationForm()
        return render(request, 'app/customerregistration.html',{'form':form})   
    def post(self,request):
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congrats! registered successfully.')
            form.save()
        else:
            messages.warning(request,'Error! Some error occurred.')
        return render(request, 'app/customerregistration.html',{'form':form})

    
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            temp = (p.quantity)*(p.product.discounted)
            amount+=temp
    total_amount = amount+shipping_amount     
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congraturations! Updated successfully.")
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})