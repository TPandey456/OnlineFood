from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import userProfile
from accounts.views import login
from .context_processors import get_cart_amounts, get_cart_counter
from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from vendor.models import OpeningHours
from django.db.models import Q

from datetime import date, datetime
from orders.forms import OrferForm
# Create your views here.


def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count=vendors.count()
    print(vendors)
    
    return render(request,'marketplace/listing.html',{"vendors":vendors, "vendor_count":vendor_count})

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_avilable=True)
        )
    )

    opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    
    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()
    
    current_opening_hours = OpeningHours.objects.filter(vendor=vendor, day=today) # current day opening hour like today is sat
   



    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    print(current_opening_hours)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items':cart_items,
        'opening_hours':  opening_hours,
        'current_opening_hours ': current_opening_hours ,
    }
    return render(request, 'marketplace/vendor_detail.html', context)   


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



def decrease_Cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                     
                    if chkCart.quantity >= 1:

                        #decrease the cart quantityx
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    
                    return JsonResponse({'status': 'Success',"cart_counter":get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart! '})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    

@login_required(login_url='login')
def cart(request):
    cart_items= Cart.objects.filter(user=request.user).order_by('created_date')  
# order by k mtlb hai ki jo bhi change krte hai vo vaise hi rhe niche n aaye list m
    return render(request,'marketplace/cart.html',{'cart_items':cart_items})


# note:cart_items= Cart.objects.filter(user=request.user)--> is lyn k mtlb hai logged in usser

def delete_Cart(request,cart_id):
     if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'}) 
        

def search(request):
    address=request.GET['address']
    latitude=request.GET['lat']
    longitude=request.GET['lng']
    radius=request.GET['radius']
    keyword=request.GET['keyword']  
    


    fetch_vendor_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_avilable=True ).values_list('vendor',flat=True)

    print(fetch_vendor_by_fooditems)

    vendors =Vendor.objects.filter(Q(id__in=fetch_vendor_by_fooditems)| Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))

    vendor_count=vendors.count()
    return render(request,'marketplace/listing.html',{'vendors':vendors, 'vendor_count':vendor_count})


@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_date')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    user_profile = userProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrferForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    context={
        'form':form,
        'cart_items':cart_items
    }
    return render(request,'marketplace/checkout.html',context)