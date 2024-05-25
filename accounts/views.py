from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages
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
    return render(request, 'accounts/registerUser.html', {'form': fm})
   
