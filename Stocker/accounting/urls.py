from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path('', views.accounting_signin_page, name="accounting_signin_page"),
    path('logout/', views.logout_page, name="logout_page"),
]
