from django import forms 
from .models import User ,userProfile
from .validators import allow_image_only

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["first_name",'last_name','username','email','password']

    def clean(self):
        cleaned_data=super(UserForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password') 

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match! "
            )
        
class userProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your address','required':'required' }))
    profile_pic=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_image_only])
    cover_pic=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_image_only])

# one way
    # latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
         model =userProfile
         fields=('profile_pic','cover_pic','address','country','state','city','pin_code','longitude',
                 'latitude')

# two way        
    def __init__(self,*args,**kwargs):
            super(userProfileForm,self).__init__(*args,**kwargs)
            for field in self.fields:
                  if field == 'latitude' or field == 'longitude':
                       self.fields[field].widget.attrs['readonly'] ='readonly'      