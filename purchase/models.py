from django.db import models
from inventory.models import Product
# from django.contrib.auth.models import User
from seller.models import Seller
from django.conf import settings


class PurchaseOrder(models.Model):
    seller = models.ForeignKey(Seller, default=1, on_delete=models.SET_DEFAULT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by_user', default=1,  on_delete=models.SET_DEFAULT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by_user', default=1,  on_delete=models.SET_DEFAULT)
    def __str__(self):
        return self.seller.name
    
class PurchaseOrderDescription(models.Model):
    item = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='product', on_delete=models.CASCADE)
    qty = models.IntegerField(blank=True, null=True)
    cost_price = models.FloatField()
    
    def __str__(self):
        return self.product.name