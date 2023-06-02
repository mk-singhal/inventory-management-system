from django.shortcuts import render, redirect
from .models import Seller, PurchaseOrderDescription, PurchaseOrder
from django.core.paginator import Paginator
from django.db.models import Q  # New
from django.db.models.functions import Lower


# Create your views here.
def purchase(request):
    # For searching the Sellers
    search_seller = request.GET.get('search_seller')
    if search_seller:
        seller = Seller.objects.filter(Q(name__icontains=search_seller))
    else:
        # If not searched, return default posts
        seller = Seller.objects.all().order_by(Lower("name"))
    
    p = Paginator(seller, 12)  # creating a paginator object
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
    
    return render(request, 'purchase/purchase.html', {'sb':4, 'page_obj':page_obj})

def add_seller(request):
    if request.method == "POST":
        instance = Seller()
        instance.name = request.POST['name']
        if (request.POST['gstin'] != ''):
            instance.gstin = request.POST['gstin']
        if (request.POST['mob_no'] != ''):
            instance.mob_no = request.POST['mob_no']
        if (request.POST['address'] != ''):
            instance.address = request.POST['address']
        if (request.POST['email'] != ''): 
            instance.email = request.POST['email']
        if bool(request.FILES.get('pic', False)) == True:
            instance.pic = request.FILES['pic']
        instance.save()
        return redirect('purchase:purchase')
    return render(request, 'purchase/addSeller.html', {'sb':4})

def edit_seller(request, seller_id):
    return render(request, 'purchase/purchase.html', {'sb':4})

def del_seller(request):
    return render(request, 'purchase/purchase.html', {'sb':4})