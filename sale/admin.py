from django.contrib import admin
from .models import SaleOrder, SaleOrderDescription, State

# Register your models here.
admin.site.register([State, SaleOrder, SaleOrderDescription])