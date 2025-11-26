from django.db import models
from core.models import AbstractModel
from product.models import Product, Color, Grid
from django.contrib.auth.models import AbstractUser
# Create your models here.

    
class User(AbstractUser):

    number = models.CharField(
        max_length=20,
        null=True,
        blank=True, 
        unique = True,         
        error_messages={
            "unique": ("A user with that number already exists."),
        },)
    region = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=False, blank=False)
    postal = models.CharField(max_length= 10, null=False, blank=False)
    cities = models.CharField(max_length=100, null=False, blank=False) 
    



class Basket(AbstractModel):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
   
    def __str__(self) :
        return self.user.email
    
class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    grid = models.ForeignKey(Grid, null=True, blank=True, on_delete=models.SET_NULL)

    quantity = models.IntegerField(default=1)

    custom_width = models.FloatField(null=True, blank=True)
    custom_height = models.FloatField(null=True, blank=True)
    custom_price = models.FloatField(null=True, blank=True)

    @property
    def total_price(self):
        if self.custom_price:
            return self.custom_price * self.quantity
        return self.product.price * self.quantity

    def __str__(self) :
        return self.basket.user.email
    
    

