from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "purchase"
urlpatterns = [
    path('', views.purchase, name="purchase"),
    path('add-seller', views.add_seller, name="add-seller"),
    path('edit-seller/<seller_id>', views.edit_seller, name="edit-seller"),
    path('del-seller/<seller_id>', views.del_seller, name="del-seller"),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]