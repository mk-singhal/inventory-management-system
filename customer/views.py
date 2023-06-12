import json
from django.shortcuts import render, redirect, HttpResponse
from .models import Customer
from django.core.paginator import Paginator
from django.db.models import Q  # New
from django.db.models.functions import Lower


# Create your views here.
def customer(request):
    # For searching the Customers
    search_customer = request.GET.get('search_customer')
    if search_customer:
        customer = Customer.objects.filter(Q(name__icontains=search_customer))
    else:
        # If not searched, return default posts
        customer = Customer.objects.all().order_by(Lower("name"))
    
    p = Paginator(customer, 12)  # creating a paginator object
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
    
    return render(request, 'customer/customer.html', {'sb':4, 'page_obj':page_obj})

def add_customer(request):
    if request.method == "POST":
        instance = Customer()
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
        return redirect('customer:customer')
    return render(request, 'customer/addCustomer.html', {'sb':4})

def edit_customer(request, customer_id):
    customer_instance = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        
        customer_instance.name = request.POST['name']

        if (request.POST['gstin'] != ''):
            customer_instance.gstin = request.POST['gstin']

        if (request.POST['mob_no'] != ''):
            customer_instance.mob_no = request.POST['mob_no']
            
        if (request.POST['address'] != ''):
            customer_instance.address = request.POST['address']
            
        if (request.POST['email'] != ''):
            customer_instance.email = request.POST['email']
            
        if bool(request.FILES.get('pic', False)) == True:
            customer_instance.pic = request.FILES['pic']
        
        customer_instance.save()
        return redirect('customer:customer')
    return render(request, 'customer/editCustomer.html', {'sb':4, 'customer':customer_instance})

def del_customer(request, customer_id):
    customer_instance = Customer.objects.get(pk=customer_id)
    customer_instance.delete()
    return redirect('customer:customer')

def get_customer(request, customer_id):
    
    customer = Customer.objects.get(pk=customer_id)
    customer_dict = {}
    customer_dict['name'] = customer.name
    customer_dict['pic_url'] = customer.pic.url
    customer_dict['gstin'] = customer.gstin
    customer_dict['mob_no'] = customer.mob_no
    customer_dict['email'] = customer.email
    customer_dict['address'] = customer.address
    
    return HttpResponse(json.dumps(customer_dict), content_type="application/json")