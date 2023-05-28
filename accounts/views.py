from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# from django.contrib

# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # return HttpResponse()
            fname = user.first_name
            email = user.email
            # return render(request, "sr/home.html", {'fname':fname, 'email':email})
            return redirect('home:home')
        else:
            messages.error(request, "Bad credentials!")
            return redirect('signin')

    return render(request, "accounts/signin.html")

def signout(request):
    logout(request)
    return redirect('home:home')