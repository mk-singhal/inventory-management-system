from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "purchase"
urlpatterns = [
    path('', views.purchase, name="purchase"),
    path('create-purchase/', views.create_purchase, name="create-purchase"),
    path('view-purchase/<purchase_order_id>/', views.view_purchase, name="view-purchase"),
    # path('edit-purchase/<purchase_order_id>/', views.edit_purchase, name="edit-purchase"),
    # path('del-purchase/<purchase_order_id>/', views.del_purchase, name="del-purchase"),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]