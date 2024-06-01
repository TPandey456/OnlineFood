from django.urls import path
from . import views
from accounts import views as v
urlpatterns = [
    path('',v.vendorDashboard, name="vendor"),
    path('profile/',views.vprofile, name='v_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/' , views.fooditems_by_category, name='fooditems_by_category'),


    #category crud url 

    path('menu-builder/category/add/', views.add_category , name='add_Category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category , name='edit_Category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category , name='delete_Category'),
]
