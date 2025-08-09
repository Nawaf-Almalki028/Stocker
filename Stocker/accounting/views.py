from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

def accounting_signin_page(request:HttpRequest):
  return render(request, "main/signin.html")

def accounting_signup_page(request:HttpRequest):
  return render(request, "main/signup.html")