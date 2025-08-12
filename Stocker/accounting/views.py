from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def accounting_signin_page(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:dashboard_home")
        else:
            messages.error(request, "signin failed, please check your credentials")

    return render(request, "main/signin.html")

def logout_page(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect("accounting:accounting_signin_page")