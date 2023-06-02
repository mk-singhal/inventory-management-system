from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderDescription

# Register your models here.
admin.site.register([PurchaseOrder, PurchaseOrderDescription])