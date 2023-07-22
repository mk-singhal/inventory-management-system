import json
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .models import Seller
from django.core.paginator import Paginator
from django.db.models import Q, ProtectedError
from django.db.models.functions import Lower
from django.contrib import messages


# Create your views here.
def seller(request):
    # For searching the Sellers
    search_seller = request.GET.get('search_seller')
    if search_seller:
        seller = Seller.objects.exclude(id=1).filter(Q(name__icontains=search_seller))
    else:
        # If not searched, return default posts
        seller = Seller.objects.all().exclude(id=1).order_by(Lower("name"))
    
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
    
    return render(request, 'seller/seller.html', {'sb':6, 'page_obj':page_obj})

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
        try:
            instance.save()
            messages.success(request, "Seller added successfully.")
            return redirect('seller:seller')
        except:
            messages.error(request, "Error, seller not added!")
    return render(request, 'seller/addSeller.html', {'sb':6})

def edit_seller(request, seller_id):
    if seller_id == 1:
      raise Http404
    try:
        seller_instance = Seller.objects.get(pk=seller_id)
    except:
        messages.error(request, "Seller not found!")
        return redirect('seller:seller')
    
    if request.method == 'POST':
        seller_instance.name = request.POST['name']
        seller_instance.gstin = request.POST['gstin']
        if (request.POST['mob_no'] == ''):
            seller_instance.mob_no = None
        else:
            seller_instance.mob_no = request.POST['mob_no']
        seller_instance.address = request.POST['address']
        seller_instance.email = request.POST['email']
        if bool(request.FILES.get('pic', False)) == True:
            seller_instance.pic = request.FILES['pic']
        try:
            seller_instance.save()
            messages.success(request, "Edits successfull.")
            return redirect('seller:seller')
        except:
            messages.error(request, "Error while editing the seller!")
    return render(request, 'seller/editSeller.html', {'sb':6, 'seller':seller_instance})

def del_seller(request, seller_id):
    if seller_id == 1:
        messages.error(request, "Access Restricted!!")
        return redirect('seller:seller')
    
    try:
        seller_instance = get_object_or_404(Seller, pk=seller_id)
    except:
        messages.error(request, "Seller not found!")
        return redirect('seller:seller')

    try:
        seller_instance.delete()
        messages.success(request, "Seller successfully removed.")
    except ProtectedError:
        messages.error(request, "Seller can't be deleted!!")
    except:
        messages.error(request, "Error while removing the seller!")
    finally:
        return redirect('seller:seller')


def get_seller(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    seller_dict = {}
    seller_dict['name'] = seller.name
    seller_dict['pic_url'] = seller.pic.url
    seller_dict['gstin'] = seller.gstin
    seller_dict['mob_no'] = seller.mob_no
    seller_dict['email'] = seller.email
    seller_dict['address'] = seller.address
    
    return HttpResponse(json.dumps(seller_dict), content_type="application/json")