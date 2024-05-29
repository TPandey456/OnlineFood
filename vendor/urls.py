from django.urls import path
from . import views
from accounts import views as v
urlpatterns = [
    path('',v.vendorDashboard, name="vendor"),
    path('profile/',views.vprofile, name='v_profile')
]
