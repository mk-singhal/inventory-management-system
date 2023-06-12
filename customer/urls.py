from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "customer"
urlpatterns = [
    path('', views.customer, name="customer"),
    # path('view-customer/', views.view_customer, name="view-customer"),
    path('add-customer/', views.add_customer, name="add-customer"),
    path('edit-customer/<customer_id>/', views.edit_customer, name="edit-customer"),
    path('del-customer/<customer_id>/', views.del_customer, name="del-customer"),
    path('get-customer/<customer_id>/', views.get_customer, name='get-customer'),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]