from django.shortcuts import render, redirect
from .models import PurchaseOrderDescription, PurchaseOrder
from inventory.models import Product
from seller.models import Seller
from django.core.paginator import Paginator
from django.db.models import Q  # New


# Create your views here.
def purchase(request):
    search_purchase = request.GET.get('search_purchase')
    if search_purchase:
        purchase_orders = PurchaseOrder.objects.filter(
            Q(seller__name__icontains=search_purchase) |
            Q(product__item__name__icontains=search_purchase)
            ).distinct()
    else:
        # If not searched, return default posts
        purchase_orders = PurchaseOrder.objects.all().order_by('created_on')
    
    p = Paginator(purchase_orders, 12)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    # print("\n\n$$$: ", [i for i in purchase_orders])
    return render(  
                    request, 
                    'purchase/purchase.html', 
                    { 
                        'sb':5,
                        'page_obj': page_obj,
                    }
                )

# Create your views here.
def view_purchase(request, purchase_order_id):
    po = PurchaseOrder.objects.get(pk=purchase_order_id)
    
    product_taxable_value_ls = []
    product_gst_ls = []
    product_price_ls = []
    # total_price_ls = []
    total_purchase_order_price = 0
    for pod in po.product.all():
        
        product_taxable_value = pod.qty * pod.cost_price
        product_taxable_value_ls.append( (round(product_taxable_value, 2)) )
        
        product_gst = (pod.item.gst/100) * (pod.qty * pod.cost_price)
        product_gst_ls.append( (round(product_gst, 2)) )
        
        product_price = ((pod.item.gst/100)+1)*(pod.qty * pod.cost_price)
        product_price_ls.append( (round(product_price, 2)) )
        
        # noqty_bill_price = ((pod.product.gst/100)+1)*(pod.noqty_bill * pod.cost_price)
        # noqty_bill_price_ls.append( (round(noqty_bill_price, 2)) )
    
        # total_price = qty_nobill_price + qty_bill_price + noqty_bill_price
        # total_price_ls.append( (round(total_price, 2)) )
        
        total_purchase_order_price += product_price
            
    return render(request, 'purchase/viewPurchase.html', {
        'sb':5, 
        'po':po,
        'product_taxable_value':product_taxable_value_ls,
        'product_gst':product_gst_ls,
        'product_price':product_price_ls,
        # 'total_price':total_price_ls,
        'total_purchase_order_price':round(total_purchase_order_price, 2),
    })

def create_purchase(request):
    product = Product.objects.all()
    seller = Seller.objects.all()
    if request.method == "POST":
        seller_id = request.POST['select_seller']
        
        total_product = request.POST['total_product']
        
        po_instance = PurchaseOrder()
        po_instance.seller = Seller.objects.get(pk=seller_id)
        po_instance.created_by = request.user
        # po_instance.updated_by = request.user
        po_instance.save()
        
        for i in range(int(total_product)):
            pod_instance = PurchaseOrderDescription()
            pod_instance.item = Product.objects.get(
                pk=request.POST[f'select_products_{i}']
            )
            pod_instance.purchase_order = po_instance
            pod_instance.qty = request.POST[f'qty_{i}']
            pod_instance.cost_price = request.POST[f'cost_price_{i}']
                        
            pod_instance.save()
        
        return redirect('purchase:view-purchase', po_instance.id)
    return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})

def edit_purchase(request, purchase_order_id):
    
    po = PurchaseOrder.objects.get(pk=purchase_order_id)
    
    product = Product.objects.all()
    seller = Seller.objects.all()
    if request.method == "POST":
        seller_id = request.POST['select_seller']
        
        total_product = int(request.POST['total_product'])
        
        po.seller = Seller.objects.get(pk=seller_id)
        po.updated_by = request.user
        po.save()
        
        i=0
        j=len(po.product.all()) - total_product
        
        for pod in po.product.all():
            if j > 0:
                pod.delete()
            else:
                break
        
        for pod in po.product.all():
            pod.item = Product.objects.get(
                pk=request.POST[f'select_products_{i}']
            )
            pod.qty = request.POST[f'qty_{i}']
            pod.cost_price = request.POST[f'cost_price_{i}']
            pod.save()
            i += 1
            
        if len(po.product.all()) < total_product:
            for _ in range(total_product - len(po.product.all())):
                pod_instance = PurchaseOrderDescription()
                pod_instance.item = Product.objects.get(
                    pk=request.POST[f'select_products_{i}']
                )
                pod_instance.purchase_order = po
                pod_instance.qty = request.POST[f'qty_{i}']
                pod_instance.cost_price = request.POST[f'cost_price_{i}']                
                
                pod_instance.save()
                i += 1
        
        return redirect('purchase:view-purchase', po.id)
    return render(request, 'purchase/editPurchase.html', {
        'sb':5, 
        'product':product,
        'seller':seller,
        'po':po
    })

def del_purchase(request, purchase_order_id):
    po = PurchaseOrder.objects.get(pk=purchase_order_id)
    po.delete()
    return redirect('purchase:purchase')