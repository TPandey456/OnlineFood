from django.contrib import admin
from menu.models import FoodItem,Category


class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":('category_name',)}
    list_display=('category_name','vendor','updated_at')
    search_fields=('category_name','vendor__vendor_name') ;""" with the help of this we can search """


class foodAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":('food_title',)}
    list_display=('food_title','category_name','vendor','price','is_avilable','updated_at')
    search_fields=('food_title','category__category_name','vendor__vendor_name','price')
# because category is foreign key thats y we use double underscore 
    list_filter=('is_avilable',)
#only one field we check is show available yes or not 


admin.site.register(Category,categoryAdmin)
admin.site.register(FoodItem,foodAdmin)