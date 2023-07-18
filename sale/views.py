from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from .models import SaleOrderDescription, SaleOrder, State
from inventory.models import Product
from customer.models import Customer
from django.core.paginator import Paginator
from django.db.models import Q, F  # New
from babel.numbers import format_currency


def calc_order_total(orders):
    order_price_ls = []
    for order in orders:
        order_price = 0
        for product in order.sale_product.all():
            order_price += (product.sell_price * product.qty * (1 - product.discount*0.01))*(1 + product.item.gst*0.01)
        order_price_ls.append(round(order_price, 2))
    return order_price_ls

# Create your views here.
def sale(request):
    if request.method == "POST":
        so = SaleOrder.objects.get(pk = request.POST['orderID'])
        so.amount_paid = request.POST['amtPaid']
        so.save()
        return redirect('sale:sale')
    
    sale_orders = SaleOrder.objects.all()
    
    search_sale = request.GET.get('search_sale')
    if search_sale:
        sale_orders = sale_orders.filter(
            Q(unreg_bill_to_name__icontains=search_sale) |
            Q(invoice_no__icontains=search_sale) |
            Q(reg_bill_to__name__icontains=search_sale) |
            Q(sale_product__item__name__icontains=search_sale)
            ).distinct()
        print("\nSearch Sale: ", search_sale, sale_orders)

    search_date = request.GET.get('search_date')
    if search_date:
        sale_orders = sale_orders.filter(
            created_on__date=search_date
            )
        print("\nSearch Date: ", search_date, sale_orders)
    
    search_due = request.GET.get('search_due')
    search_partial = request.GET.get('search_partial')
    search_paid = request.GET.get('search_paid')
    
    sale_orders_due = SaleOrder.objects.none()
    sale_orders_partial = SaleOrder.objects.none()
    sale_orders_paid = SaleOrder.objects.none()
    flg = False
    
    date_from = datetime.now() - timedelta(days=1)
    if search_due == 'on':
        sale_orders_due = sale_orders.filter(
            amount_paid__gte=0,
            amount_paid__lt=0.01,
            created_on__lte=date_from
            )
        # print("\nSearch DUE: ", search_due, sale_orders)
        flg = True
    
    if search_partial == 'on':
        sale_orders_partial = sale_orders.filter(
            amount_paid__lt=F('order_price'),
            amount_paid__gt=0,
            )
        # print("\nSearch Partial: ", search_partial, sale_orders)
        flg = True
    
    if search_paid == 'on':
        sale_orders_paid = sale_orders.filter(
            amount_paid=F('order_price'),
            )
        # print("\nSearch Paid: ", search_paid, sale_orders)
        flg = True
        
    if flg:
        sale_orders_tmp = sale_orders_due.union(sale_orders_partial)
        sale_orders = sale_orders_tmp.union(sale_orders_paid)
    sale_orders = sale_orders.order_by('-created_on')
    
    p = Paginator(sale_orders, 12)  # creating a paginator object
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
    
    # print('\n\n%%%%', bool(search_sale), bool(search_date), search_due, search_partial, search_paid)
    return render(  
                    request, 
                    'sale/sale.html', 
                    { 
                        'sb':3,
                        'sale_search': search_sale,
                        'date_search': search_date,
                        'due_status': search_due,
                        'partial_status': search_partial,
                        'paid_status': search_paid,
                        'page_obj': page_obj,
                    }
                )

# Create your views here.
def view_sale(request, sale_order_id):
    so = SaleOrder.objects.get(pk=sale_order_id)
    
    # taxable_value_ls = []
    # halfgst_value_ls = []
    # fullgst_value_ls = []
    # total_value_ls = []
    total_taxable_value = 0
    total_halfgst_value = 0
    total_fullgst_value = 0
    # sum_total_value = 0
    
    for product in so.sale_product.all():
        total_taxable_value += product.taxable_value
        total_fullgst_value += product.gst_value
        total_halfgst_value += product.gst_value/Decimal(2)
        
    return render(request, 'sale/viewSale.html', {
        'sb':3,
        'so':so,
        'total_taxable_value':total_taxable_value,
        'total_halfgst_value':total_halfgst_value,
        'total_fullgst_value':total_fullgst_value,
    })

def increment_invoice_number():
    initial_str = ''
    import datetime
    x = datetime.datetime.now(datetime.timezone.utc)
    if int(x.strftime("%m")) > 3:
        initial_str = str(x.strftime("%Y")) + '-' + str(int(x.strftime("%y"))+1)
    else:
        initial_str = str(int(x.strftime("%Y"))-1) + '-' + str(x.strftime("%y"))
    initial_str += '/' + str(x.strftime("%m")) + '/'


    last_invoice = SaleOrder.objects.all().order_by('id').last()
    invoice_num = '/000'
    if last_invoice and (x.month == last_invoice.created_on.month):
        invoice_num = last_invoice.invoice_no
    invoice_int = int(invoice_num.split('/')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_int = "{:03d}".format(new_invoice_int)
    new_invoice_no = initial_str + str(new_invoice_int)
    return new_invoice_no

def create_sale(request):
    product = Product.objects.all()
    customer = Customer.objects.all().exclude(id=1)
    state = State.objects.all().exclude(id=1)
    sale_choices = SaleOrder.GSTSaleType
    invoice_number = increment_invoice_number()
    
    if request.method == "POST":
        print('#########', request.POST)
        print("\n\n$$$$$$$$$", request.POST['customer_registered'])
        so_instance = SaleOrder()
        so_instance.invoice_no = invoice_number
        so_instance.gst_sale_type = request.POST['gst_sale_type']
        so_instance.created_by = request.user
        
        if request.POST['customer_registered'] == 'yes':
            customer_id = request.POST['select_customer']
            so_instance.reg_bill_to = Customer.objects.get(pk=customer_id)
            if request.POST['ship_to_gstin'] != '': so_instance.reg_ship_to_gstin = request.POST['ship_to_gstin']
        else:
            so_instance.unreg_bill_to_name = request.POST['bill_to_name']
            so_instance.unreg_bill_to_address1 = request.POST['bill_to_add1']
            so_instance.unreg_bill_to_address2 = request.POST['bill_to_add2']
            so_instance.unreg_bill_to_state = State.objects.get(pk=request.POST['bill_to_state'])
            so_instance.unreg_ship_to_state = State.objects.get(pk=request.POST['ship_to_state'])

        so_instance.ship_to_name = request.POST['ship_to_name']
        so_instance.ship_to_address1 = request.POST['ship_to_add1']
        so_instance.ship_to_address2 = request.POST['ship_to_add2']
        if request.POST['transport_name'] != '': so_instance.transport_name = request.POST['transport_name']
        if request.POST['transport_id'] != '': so_instance.transport_id = request.POST['transport_id']
        if request.POST['transport_mode'] != '': so_instance.transport_mode = request.POST['transport_mode']
        if request.POST['transport_vehicle'] != '': so_instance.transport_veh_no = request.POST['transport_vehicle']
        if request.POST['transport_gstin'] != '': so_instance.transport_gstin = request.POST['transport_gstin']
        
        so_instance.save()
        total_product = request.POST['total_product']
        total_order_price = 0
        
        for i in range(int(total_product)):
            sod_instance = SaleOrderDescription()
            sod_instance.item = Product.objects.get(
                pk=request.POST[f'select_products_{i}']
            )
            sod_instance.sale_order = so_instance
            sod_instance.qty = int(request.POST[f'sale_qty_{i}'])
            sod_instance.sell_price = float(request.POST[f'sale_rate_{i}'])
            sod_instance.discount = float(request.POST[f'sale_dis_{i}'])
            sod_instance.taxable_value = round(( (sod_instance.qty*sod_instance.sell_price)*(1-sod_instance.discount) ), 2)
            sod_instance.gst_value = round(( (sod_instance.item.gst*0.01)*(sod_instance.qty*sod_instance.sell_price) ), 2)
            sod_instance.product_price = round(( (sod_instance.qty*sod_instance.sell_price)*(1-sod_instance.discount)*(1+sod_instance.item.gst*0.01) ), 2)
            total_order_price += sod_instance.product_price
            sod_instance.save()
        
        so_instance.order_price = round(total_order_price, 2)
        so_instance.save()
        return redirect('sale:view-sale', so_instance.id)
    return render(request, 'sale/createSale.html', 
                  {'sb':3, 
                   'product':product, 
                   'customer':customer, 
                   'state':state, 
                   'sale_choices':sale_choices,
                   'invoice_number':invoice_number,
                   }
                  )

def edit_sale(request, sale_order_id):
    
    po = SaleOrder.objects.get(pk=sale_order_id)
    
    product = Product.objects.all()
    customer = Customer.objects.all()
    if request.method == "POST":
        customer_id = request.POST['select_customer']
        
        total_product = int(request.POST['total_product'])
        
        po.customer = Customer.objects.get(pk=customer_id)
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
                pod_instance = SaleOrderDescription()
                pod_instance.item = Product.objects.get(
                    pk=request.POST[f'select_products_{i}']
                )
                pod_instance.sale_order = po
                pod_instance.qty = request.POST[f'qty_{i}']
                pod_instance.cost_price = request.POST[f'cost_price_{i}']                
                
                pod_instance.save()
                i += 1
        
        return redirect('sale:view-sale', po.id)
    return render(request, 'sale/editSale.html', {
        'sb':3,
        'product':product,
        'customer':customer,
        'po':po
    })