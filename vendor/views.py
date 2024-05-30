from django.shortcuts import get_object_or_404,render,redirect
from .forms import vendorForm 
from accounts.forms import userProfileForm

from accounts.models import userProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
# Create your views here.

@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(userProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)
# profile and vendore both are instance


    if request.method == "POST":
        profile_form=userProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form=vendorForm(request.POST, request.FILES, instance=vendor)
# so if both the form are valid then we stor the data
        
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Updated')
            return redirect('v_profile')       
        else:
            print(profile_form.errors)    
            print(vendor_form.errors)    
    else:
        profile_form =userProfileForm(instance=profile)
        vendor_form = vendorForm(instance=vendor)


    return render(request,'vendor/vprofile.html',{'profile_form':profile_form,'vendor_form':vendor_form,'profile':profile,'vendor':vendor})