from django.contrib import admin
from .models import Payment, OrderedFood,Order
# Register your models here.

class orderFood(admin.TabularInline):  # this will give data in  tabulForm  inside the admin panel
    model = OrderedFood 
    readonly_fields =('order','payment', 'user','fooditem','quantity','price','amount')
    extra=0

class orderAdmin(admin.ModelAdmin):
    list_display=['order_number', 'name','phone','email','total','payment_method','status','is_ordered']
    inlines = [orderFood] 

admin.site.register(Payment)
admin.site.register(OrderedFood)
admin.site.register(Order,orderAdmin)