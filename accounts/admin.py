from django.contrib import admin
from .models import User,userProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomAdminUser(UserAdmin):
    list_display=('email','username','first_name','is_active','role')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(User,CustomAdminUser)
admin.site.register(userProfile)


