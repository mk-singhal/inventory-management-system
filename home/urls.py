from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

app_name = "home"
urlpatterns = [
    path('', views.home, name="home"),
    # path('register', views.register, name="register"),
    # path('logout', views.logout, name="logout"),
    # path('activate/<uidb64>/<token>', views.activate, name="activate")
]