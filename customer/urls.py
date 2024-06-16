from django.urls import path
from accounts import views  as v

from . import views

urlpatterns = [
    path('',v.customerDashboard,name='customer'),
    path('profile/',views.cprofile, name='cprofile')
]
