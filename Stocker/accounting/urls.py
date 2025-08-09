from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path('signin/', views.accounting_signin_page, name="accounting_signin_page"),
    path('signup/', views.accounting_signup_page, name="accounting_signup_page"),
]
