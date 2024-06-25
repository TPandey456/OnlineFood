import simplejson as json
from django.shortcuts import render,get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import userProfileForm,UserInfoForm
from accounts.models import userProfile
from django.contrib import messages

from orders.models import Order,OrderedFood
# Create your views here.

login_required(login_url='login')
def cprofile(request):
    profile =get_object_or_404(userProfile,user=request.user)
    # print('profile',profile)

    if request.method == 'POST':   
        profile_form = userProfileForm(request.POST, request.FILES , instance=profile)
        user_form = UserInfoForm(request.POST , instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = userProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
   
    return render(request,'customers/cprofile.html',context)

# need to initializr the two forms one is updating the user profile and another one is for updating the user's basic information such as fist_name
# last_name & phone_no those field are inside the user model and also do not allow the user to change name email and other field are userprofile model


def my_orders(request):
    orders= Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at') 

    context={
        'orders' : orders,

    }
    return render(request,'customers/my_order.html',context)


def order_detail(request,order_number):
    
    try:
        order =Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        
        subtotal=0
        for  item in ordered_food:
           subtotal += (item.price * item.quantity)
        tax_data= json.loads((order.tax_data))
        context={
            'order' : order ,
            'ordered_food' : ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data

        }
    except:
        return redirect('customer')
    return render(request,'customers/order_detail.html',context)