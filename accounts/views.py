from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User,userProfile
from django.contrib import messages
from vendor.forms import vendorForm

def registerUser(request):
    if request.method == "POST":
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
    if request.method == "POST":
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
