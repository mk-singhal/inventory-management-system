from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "seller"
urlpatterns = [
    path('', views.seller, name="seller"),
    # path('view-seller/', views.view_seller, name="view-seller"),
    path('add-seller/', views.add_seller, name="add-seller"),
    path('edit-seller/<seller_id>/', views.edit_seller, name="edit-seller"),
    path('del-seller/<seller_id>/', views.del_seller, name="del-seller"),
    path('get-seller/<seller_id>/', views.get_seller, name='get-seller'),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]