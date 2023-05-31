from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "inventory"
urlpatterns = [
    path('', views.inventory, name="inventory"),
    path('add-product', views.add_product, name="add-product"),
    path('edit-product/<product_id>', views.edit_product, name="edit-product"),
    path('del-product/<product_id>', views.delete_product, name="del-product"),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]