from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.myaccount),
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor , name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_vali/<uidb64>/<token>/',views.reset_password_vali,name='reset_password_vali'),
    path('reset_password/',views.rest_password,name='reset_password'),

    path('vendor/',include('vendor.urls'))
]
    