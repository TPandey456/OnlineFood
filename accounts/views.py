
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User,userProfile
from django.contrib import messages,auth
from vendor.forms import vendorForm
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.template.defaultfilters import slugify
from vendor.models import Vendor
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

@csrf_exempt
def registerUser(request):
   def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myaccount')
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

            mail_subject="Please activate your account! "
            email_template="accounts/emails/account_verify_email.html"
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request,"Your account registration is complete! Please await approval.")
            return redirect('registerVendor')   
        else:
            print("invalid")
            print(fm.errors)
    else:
       fm=UserForm()
       v_fm=vendorForm()
    return render(request,'accounts/registerVendor.html',{'form':fm,"v_form":v_fm})

# @csrf_exempt   

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = vendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = userProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form =vendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)




def activate(request,uidb64,token):
    try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
       user=None  

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congrulations! Your account is activated")
        return redirect('myaccount')
    else:
        messages.error(request,"Invalid activation link!")
        return redirect('myaccount')
    

@csrf_exempt
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
@csrf_exempt
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


def forgot_password(request):
    if request.method == "POST":
        email=request.POST['email']; """ user enter mail we need exact """
        
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            mail_subject ="Rest Your Password"
            email_template="accounts/emails/reset_password_email.html"
            # this goes dynamic

            #send reset password email with the help dynamic
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"Your password reset link has been emailed to you.")
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgot_password')

    return render(request,'accounts/forgot_password.html')



def reset_password_vali(request,uidb64,token):
    try:
       uid=urlsafe_base64_decode(uidb64).decode()
       user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
       user=None  

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] =uid
        messages.info(request,"Please reset your Password")
        return redirect('reset_password')
    else:
        messages.error(request,"This link has been expired!")
        return redirect('myaccount')

def rest_password(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password == confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,"Password reset successful!")
            return redirect('login')
        else:
                messages.error(request,"Password does not match!")
                return redirect('reset_password')
    return render(request,'accounts/rest_password.html')