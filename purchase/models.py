from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=50)
    gstin = models.CharField(max_length=15, blank=True, null=True, unique=True)
    mob_no = models.IntegerField(blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    pic = models.ImageField(default='defaultUser.png', upload_to='seller_pics')

class PurchaseOrder(models.Model):
    seller = models.ForeignKey(Seller, default=1, on_delete=models.SET_DEFAULT)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_by = models.ForeignKey(User, default=1,  on_delete=models.SET_DEFAULT)
    
class PurchaseOrderDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    qty_nobill = models.IntegerField(blank=True, null=True)
    qty_bill = models.IntegerField(blank=True, null=True)
    noqty_bill = models.IntegerField(blank=True, null=True)
    cost_price = models.FloatField()