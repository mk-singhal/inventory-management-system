from django.shortcuts import render, redirect
from .models import Product
from django.core.paginator import Paginator
from django.db.models import Q  # New
from django.db.models.functions import Lower


# Create your views here.
def inventory(request):
    # For searching the products
    search_product = request.GET.get('search_product')
    if search_product:
        product = Product.objects.filter(Q(name__icontains=search_product) | Q(hsn_code__icontains=search_product))
    else:
        # If not searched, return default posts
        product = Product.objects.all().order_by(Lower("name"))
    
    p = Paginator(product, 12)  # creating a paginator object
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
    # context = {'page_obj': page_obj}
    return render(request, 'inventory/inventory.html', {'sb':2, 'page_obj': page_obj})


def add_product(request):
    if request.method == 'POST':
        # print("\n\n##################", request.POST, request.FILES['img'])
        instance = Product()
        instance.name = request.POST['name']
        instance.pic = request.FILES['img']
        instance.hsn_code = request.POST['hsn']
        instance.qty_actual = request.POST['actual_qty']
        instance.qty_billed = request.POST['gst_qty']
        instance.min_stock_alarm = request.POST['min_stock_alarm']
        instance.surplus_alarm = request.POST['surplus_alarm']
        instance.defecit_alarm = request.POST['defecit_alarm']
        instance.measuring_unit_1 = request.POST['mu_1']
        if (request.POST['mu_2'] != ''): 
            instance.measuring_unit_2 = request.POST['mu_2']
        if (request.POST['mr'] != ''): 
            instance.measuring_unit_relation = request.POST['mr']
        instance.price = request.POST['price']
        instance.gst = request.POST['gst']
        instance.save()
        
        return redirect('inventory:inventory')
    return render(request, 'inventory/addProduct.html', {'sb':2})

def delete_product(request, product_id):
    product_instance = Product.objects.get(pk=product_id)
    product_instance.delete()
    return redirect('inventory:inventory')

def edit_product(request, product_id):
    product_instance = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        # print("\n\n##################", request.POST, "\n$$$$$$$$", bool(request.FILES.get('img', False)))
        product_instance.name = request.POST['name']
        if bool(request.FILES.get('img', False)) == True:
            product_instance.pic = request.FILES['img']
        product_instance.hsn_code = request.POST['hsn']
        product_instance.qty_actual = request.POST['actual_qty']
        product_instance.qty_billed = request.POST['gst_qty']
        product_instance.min_stock_alarm = request.POST['min_stock_alarm']
        product_instance.surplus_alarm = request.POST['surplus_alarm']
        product_instance.defecit_alarm = request.POST['defecit_alarm']
        product_instance.measuring_unit_1 = request.POST['mu_1']
        if (request.POST['mu_2'] == ''): 
            product_instance.measuring_unit_2 = None
            product_instance.measuring_unit_relation = None
        else:
            product_instance.measuring_unit_2 = request.POST['mu_2']
            product_instance.measuring_unit_relation = request.POST['mr']
        product_instance.price = request.POST['price']
        product_instance.gst = request.POST['gst']
        product_instance.save()
        return redirect('inventory:inventory')
        
    return render(request, 'inventory/editProduct.html', {'sb':2, 'product':product_instance})