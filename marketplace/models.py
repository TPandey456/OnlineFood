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
 
        