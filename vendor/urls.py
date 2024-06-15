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

    #food item crud
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food , name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food , name='delete_food'),


    #opening hour
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),
]
