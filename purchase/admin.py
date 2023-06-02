from django.contrib import admin
from .models import Seller, PurchaseOrder, PurchaseOrderDescription

# Register your models here.
admin.site.register([Seller, PurchaseOrder, PurchaseOrderDescription])