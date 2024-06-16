from django.shortcuts import render,get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import userProfileForm,UserInfoForm
from accounts.models import userProfile
from django.contrib import messages
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