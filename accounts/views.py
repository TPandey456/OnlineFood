from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User,userProfile
from django.contrib import messages,auth
from vendor.forms import vendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

#if vendor accessing customer page 

#user passes test decorator should triggered just below the
def check_role_vendor(user):
    if user.role == 1 :
        return True
    else:
        raise PermissionDenied

#if customer accessing vendor page 
def check_role_customer(user):
    if user.role == 2 :
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('dashboard')
    elif request.method == "POST":
        fm = UserForm(request.POST)
        if fm.is_valid():
            fnm = fm.cleaned_data['first_name']
            lnm = fm.cleaned_data['last_name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            usernm = fm.cleaned_data['username']
            user = User.objects.create_user(first_name=fnm, last_name=lnm, email=em, password=pw, username=usernm)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"Account has been registered successfully! ")
            return redirect('registerUser')     
        else:
            print(fm.errors)
    else:          
        fm = UserForm()            
    return render(request, 'accounts/registerUser.html', {'form': fm,})
   
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('dashboard')
    elif request.method == "POST":
        fm= UserForm(request.POST)
        v_fm=vendorForm(request.POST, request.FILES)
        if fm.is_valid() and v_fm.is_valid:
            fnm = fm.cleaned_data['first_name']
            lnm = fm.cleaned_data['last_name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            usernm = fm.cleaned_data['username']
            user = User.objects.create_user(first_name=fnm, last_name=lnm, email=em, password=pw, username=usernm)
            user.role = User.VENDOR
            user.save()
            vendor = v_fm.save(commit=False)
            vendor.user=user
            user_profile= userProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your account registration is complete! Please await approval.")
            return redirect('registerVendor')   
        else:
            print("invalid")
            print(fm.errors)
    else:
       fm=UserForm()
       v_fm=vendorForm()
    return render(request,'accounts/registerVendor.html',{'form':fm,"v_form":v_fm})

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myaccount')
    
    elif request.method == "POST":
        em=request.POST['email']
        pw=request.POST['password']

        user=auth.authenticate(email=em,password=pw)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in.")
            return redirect('myaccount')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.warning(request,"Your are logged out")
    return redirect('login')

@login_required(login_url='login') 
def myaccount(request):
    user= request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login') 
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request,'accounts/customerDashboard.html')


@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')