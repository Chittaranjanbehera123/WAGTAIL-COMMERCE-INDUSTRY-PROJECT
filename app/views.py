from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, User
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404

# ClassBase View
class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        laptops = Product.objects.filter(category='L')
        headphones = Product.objects.filter(category='H')
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles, 'laptops':laptops, 'headphones':headphones, 'totalitem':totalitem})


# ClassBase View
class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        else:
            item_already_in_cart = False
        
        return render(request, 'app/productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart
        })


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')
        
       
#Plus
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity += 1  
            c.save()  

            # Calculate the total amount for the cart
            amount = 0.0
            shipping_amount = 70.0
            cart_products = Cart.objects.filter(user=request.user)  
            
            for p in cart_products:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount':amount + shipping_amount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

   
# Minus
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity -= 1  
            c.save()  

            # Calculate the total amount for the cart
            amount = 0.0
            shipping_amount = 70.0
            cart_products = Cart.objects.filter(user=request.user)  
            
            for p in cart_products:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount
            

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount':amount + shipping_amount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
    
# Remove
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))  
            c.delete()  

            # Calculate the total amount for the cart
            amount = 0.0
            shipping_amount = 70.0
            cart_products = Cart.objects.filter(user=request.user)  
            
            for p in cart_products:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount

            data = {
                'amount': amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

            

def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})


@login_required
def orders(request):
    if not request.user.is_authenticated:
        return render(request, 'app/not_authenticated.html')  
    op = OrderPlaced.objects.filter(user=request.user)
    
    return render(request, 'app/orders.html', {'order_placed': op})


#Mobiles
def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data in ['Samsung', 'OnePlus']:
        mobiles = Product.objects.filter(category='M', brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discounted_price__lt=30000)
    elif data == 'Above':
        mobiles = Product.objects.filter(category='M', discounted_price__gt=10000)
    else:
        mobiles = Product.objects.filter(category='M')
        
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


#laptops
def laptop(request, data=None):
    if data is None:
        laptops = Product.objects.filter(category='L')
    elif data in ['Samsung Galaxy', 'Apple']:
        laptops = Product.objects.filter(category='L', brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L', discounted_price__lt=80000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L', discounted_price__gt=10000)
    else:
        laptops = Product.objects.filter(category='L')

    return render(request, 'app/laptop.html', {'laptops': laptops})


#Headphones
def headphone(request, data=None):
    if data == 'all' or data is None:
        headphones = Product.objects.filter(category='H')
    elif data in ['headphone', 'headphone']:
        headphones = Product.objects.filter(category='H', brand=data)
    elif data == 'below':
        headphones = Product.objects.filter(category='H', discounted_price__lt=1800)
    elif data == 'above':
        headphones = Product.objects.filter(category='H', discounted_price__gt=2000)
    else:
        headphones = Product.objects.filter(category='H')

    return render(request, 'app/headphone.html', {'headphones': headphones})




# classbase View
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Registered Successfully')
            return redirect('success_url')  

        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
#functionBase Views   
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0  

    for item in cart_items:
        amount += item.quantity * item.product.discounted_price

    total_amount = amount + shipping_amount if cart_items.exists() else 0

    return render(request, 'app/checkout.html', {
        'add': addresses, 
        'totalamount': total_amount, 
        'cart_items': cart_items
    })
    
    

@login_required    
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")



# Define your view classBase Views
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()  
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    # Define the POST method to handle form submission
    def post(self, request):
        form = CustomerProfileForm(request.POST)  
        if form.is_valid():  
            usr = request.user  
            name = form.cleaned_data['name']  
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            
            customer = Customer.objects.create(
                user=usr,    
                    name= name,
                    locality = locality,
                    city = city,
                    state = state,
                    zipcode = zipcode
                
            )
            
            messages.success(request, 'Congratulations! Profile updated successfully')
            return redirect('profile')  
        
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})