from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as v
urlpatterns = [ 
    path('admin/', admin.site.urls),

    path('', views.home,name="home"),

    path('',include('accounts.urls')),

    path('marketplace/', include('marketplace.urls')),

    #cart url 
    path('cart/', v.cart, name='cart'),

   #search 
   path('search/', v.search, name='search'),

   #checkout 
   path('checkout/', v.checkout, name='checkout'),

   #orders 

   path('orders/', include('orders.urls'),)


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    