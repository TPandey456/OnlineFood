from django import forms 

from .models import Order 

class OrferForm(forms.ModelForm):
    class Meta:
        model = Order 
        fields = ['first_name','last_name','phone','email','address','country','city','state','pin_code']