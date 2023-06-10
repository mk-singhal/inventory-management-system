from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User
from seller.models import Seller
from inventory.models import Product


class PurchaseOrder(models.Model):
    seller = models.ForeignKey(Seller, default=1, on_delete=models.SET_DEFAULT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by_user', default=1,  on_delete=models.SET_DEFAULT)
    updated_by = models.ForeignKey(User, related_name='updated_by_user', default=1,  on_delete=models.SET_DEFAULT)
    def __str__(self):
        # return self.seller.name
        return self.seller.name
    
class PurchaseOrderDescription(models.Model):
    item = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='product', on_delete=models.CASCADE)
    # qty_nobill = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    # noqty_bill = models.IntegerField(blank=True, null=True)
    cost_price = models.FloatField()
    
    def __str__(self):
        return self.product.name