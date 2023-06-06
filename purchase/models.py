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
    # updated_by = models.ForeignKey(User, default=1,  on_delete=models.SET_DEFAULT)
    def __str__(self):
        # return self.seller.name
        return self.seller.name
    
class PurchaseOrderDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='all_purchase_product', on_delete=models.CASCADE)
    qty_nobill = models.IntegerField(blank=True, null=True)
    qty_bill = models.IntegerField(blank=True, null=True)
    noqty_bill = models.IntegerField(blank=True, null=True)
    cost_price = models.FloatField()
    
    def __str__(self):
        return self.product.name
    
def make_dict(po, pod):
    result = {'purchase_order_id': po.id, 'Seller': po.seller.name}
    ls = [p.id for p in pod]
    result['purchase_order_description_ids'] = ls
    # tmp = []
    # for id in ls:
    #     tmp.append([PurchaseOrderDescription.objects.get(pk=id).product.name])
    #     tmp.append([PurchaseOrderDescription.objects.get(pk=id).qty_nobill])
    #     tmp.append([PurchaseOrderDescription.objects.get(pk=id).qty_bill])
    #     tmp.append([PurchaseOrderDescription.objects.get(pk=id).noqty_bill])
    #     tmp.append([PurchaseOrderDescription.objects.get(pk=id).cost_price])
    # result['product_name'] = tmp[0]
    # result['Qty without Bill'] = tmp[1]
    # result['Qty with Bill'] = tmp[2]
    # result['Only Bill'] = tmp[3]
    # result['Cost per Unit'] = tmp[4]
    # result['qty_nobill'] = po.PurchaseOrderDescription.objects.get(pk=po).qty_nobill
    # result['departments_ids'] = [d.id for d in departments]
    return result

def create_structure():
    result = [make_dict(po, po.all_purchase_product.all()) for po in PurchaseOrder.objects.all()]
    return result