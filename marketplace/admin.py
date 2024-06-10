from django.contrib import admin

from marketplace.models import Cart

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display=('user','fooditem','quantity','updated_Date')
admin.site.register(Cart,CartAdmin)