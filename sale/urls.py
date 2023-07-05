from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "sale"
urlpatterns = [
    path('', views.sale, name="sale"),
    path('create-sale/', views.create_sale, name="create-sale"),
    path('view-sale/<sale_order_id>/', views.view_sale, name="view-sale"),
    path('edit-sale/<sale_order_id>/', views.edit_sale, name="edit-sale"),
    # path('del-sale/<sale_order_id>/', views.del_sale, name="del-sale"),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]