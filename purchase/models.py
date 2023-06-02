from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User
from seller.models import Seller
from inventory.models import Product


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