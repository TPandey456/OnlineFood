from django.db import models
from accounts.models import User

from menu.models import FoodItem

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    fooditem=models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_Date=models.DateTimeField(auto_now_add=True) 


    def __unicode__(self):
        self.user 
        # user is phone key that's y we define unicode a return self taught user also this isa string representation 
 
        
class Tax(models.Model):
    tax_type= models.CharField(max_length=20, unique=True)
    tax_percentage= models.DecimalField(decimal_places=2, max_digits=4,verbose_name='Tax Percentage(%)')
    is_active= models.BooleanField(default=True)

    class Meta:
        verbose_name_plural ='Tax' #in admin portal name chane Tax instead of Taxs

    def __str__(self):
        return self.tax_type 
    
