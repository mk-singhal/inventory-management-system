from django.db import models
from inventory.models import Product
# from django.contrib.auth.models import User
from django.conf import settings
from customer.models import Customer

class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    def __str__(self):
        return self.name
    
def get_del_customer():
    return Customer.objects.get(pk=1)

class SaleOrder(models.Model):
    
    GSTSaleType = (
        ('1', 'Intra-State (SGST & CGST)'),
        ('2', 'Intra-State (UTGST)'),
        ('3', 'Inter-State (IGST)'),
    )
    gst_sale_type = models.CharField(max_length=10,choices=GSTSaleType,default=1)
    
    pay_status_choices = (
            ('1', 'Unpaid'),
            # ('2', 'Due'),
            ('3', 'Partial'),
            ('4', 'Paid'),
        )
    pay_status = models.CharField(max_length=10,choices=pay_status_choices,default=1)    
    
    reg_bill_to = models.ForeignKey(Customer, on_delete=models.SET(get_del_customer), blank=True, null=True)
    
    unreg_bill_to_name = models.CharField(max_length=50, blank=True, null=True)
    unreg_bill_to_address1 = models.CharField(max_length=50, blank=True, null=True)
    unreg_bill_to_address2 = models.CharField(max_length=50, blank=True, null=True)
    unreg_bill_to_state = models.ForeignKey(State, related_name='bill_to_sale_order', default=1, on_delete=models.SET_DEFAULT, blank=True, null=True)
    
    ship_to_name = models.CharField(max_length=50, null=True, blank=True)
    ship_to_address1 = models.CharField(max_length=50, null=True, blank=True)
    ship_to_address2 = models.CharField(max_length=50, null=True, blank=True)
    reg_ship_to_gstin = models.CharField(max_length=50, null=True, blank=True)
    unreg_ship_to_state = models.ForeignKey(State, related_name='ship_to_sale_order', default=1, on_delete=models.SET_DEFAULT, null=True, blank=True)

    transport_name = models.CharField(max_length=50, null=True, blank=True)
    transport_id = models.CharField(max_length=50, null=True, blank=True)
    transport_mode = models.CharField(max_length=50, null=True, blank=True)
    transport_veh_no = models.CharField(max_length=50, null=True, blank=True)
    transport_gstin = models.CharField(max_length=50, null=True, blank=True)

    invoice_no = models.CharField(max_length=16)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saleorder_created_by_user', default=1,  on_delete=models.SET_DEFAULT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saleorder_updated_by_user', default=1,  on_delete=models.SET_DEFAULT)
    
    def __str__(self):
        if self.reg_bill_to:
            return self.reg_bill_to.name
        else:
            return self.unreg_bill_to_name
    

class SaleOrderDescription(models.Model):
    item = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale_order = models.ForeignKey(SaleOrder, related_name='sale_product', on_delete=models.CASCADE)
    qty = models.IntegerField(blank=True, null=True)
    sell_price = models.FloatField()
    discount = models.FloatField()
    
    def __str__(self):
        return self.item.name