from django.shortcuts import render, redirect
from .models import Product

# Create your views here.
def inventory(request):
    product = Product.objects.all()
    return render(request, 'inventory/inventory.html', {'sb':2, 'products':product})


def add_product(request):
    if request.method == 'POST':
        print("\n\n##################", request.POST, request.FILES['img'])
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
        print("\n\n##################", request.POST, "\n$$$$$$$$", type(request.POST['mr']))
        product_instance.name = request.POST['name']
        if bool(request.FILES.get('filepath', False)) == True:
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