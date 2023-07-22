from django.shortcuts import render, redirect
from .models import PurchaseOrderDescription, PurchaseOrder
from inventory.models import Product
from seller.models import Seller
from django.core.paginator import Paginator
from django.db.models import Q  # New
from django.contrib import messages


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
    try:
        po = PurchaseOrder.objects.get(pk=purchase_order_id)
    except:
        messages.error(request, "Purchase-Order not found!")
        return redirect('purchase:purchase')
    
    product_taxable_value_ls = []
    product_gst_ls = []
    product_price_ls = []
    total_purchase_order_price = 0
    
    for pod in po.product.all():
        
        product_taxable_value = pod.qty * pod.cost_price
        product_taxable_value_ls.append( (round(product_taxable_value, 2)) )
        
        product_gst = (pod.item.gst/100) * (pod.qty * pod.cost_price)
        product_gst_ls.append( (round(product_gst, 2)) )
        
        product_price = ((pod.item.gst/100)+1)*(pod.qty * pod.cost_price)
        product_price_ls.append( (round(product_price, 2)) )
        
        total_purchase_order_price += product_price
            
    return render(request, 'purchase/viewPurchase.html', {
        'sb':5, 
        'po':po,
        'product_taxable_value':product_taxable_value_ls,
        'product_gst':product_gst_ls,
        'product_price':product_price_ls,
        'total_purchase_order_price':round(total_purchase_order_price, 2),
    })

def create_purchase(request):
    product = Product.objects.all()
    seller = Seller.objects.all()
    
    if request.method == "POST":
        seller_id = request.POST['select_seller']
        total_product = request.POST['total_product']
        
        po_instance = PurchaseOrder()
    
        try:
            po_instance.seller = Seller.objects.get(pk=seller_id)
        except:
            messages.error(request, "Seller not Found!!")
            return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})
    
        po_instance.created_by = request.user
        try:
            po_instance.save()
        except:
            messages.error(request, "Error, purchase order not created!")
            return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})
        
        for i in range(int(total_product)):
            pod_instance = PurchaseOrderDescription()
            try:
                inventory_product = Product.objects.get(
                    pk=request.POST[f'select_products_{i}']
                )
                pod_instance.item = inventory_product
            except:
                messages.error(request, "Product not found!")
                po_instance.delete()
                return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})

            pod_instance.purchase_order = po_instance
            pod_instance.qty = request.POST[f'qty_{i}']
            pod_instance.cost_price = request.POST[f'cost_price_{i}']
            try:
                pod_instance.save()
            except:
                po_instance.delete()
                messages.error(request, "Error while adding items, purchase order not created!")
                return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})
        
        try:
            # Update the Quantity in the Inventory model --> Product table
            po = PurchaseOrder.objects.get(pk=po_instance.id)
            for pod in po.product.all():
                inventory_product = Product.objects.get(pk=pod.item.id)
                inventory_product.qty += int(pod.qty)
                inventory_product.save()
                messages.success(request, "Purchase order created successfully.")
        except:
            messages.error(request, "Error occured while updating quantity!!")
        finally:
            return redirect('purchase:view-purchase', po_instance.id)
    return render(request, 'purchase/createPurchase.html', {'sb':5, 'product':product, 'seller':seller})