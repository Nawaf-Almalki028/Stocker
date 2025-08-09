from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

def main_home_page(request:HttpRequest):
  return render(request, "main/index.html")

def main_products_page(request:HttpRequest):
  return render(request, "products.html")