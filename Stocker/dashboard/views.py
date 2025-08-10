from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

def dashboard_home(request:HttpRequest):
  return render(request, "main/dash_home.html")

def dashboard_categ(request:HttpRequest):
  return render(request, "main/categ_home.html")

def dashboard_prod(request:HttpRequest):
  return render(request, "main/prod_home.html")

def dashboard_suppliers(request:HttpRequest):
  return render(request, "products.html")