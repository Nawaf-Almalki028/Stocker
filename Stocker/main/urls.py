from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.main_products_page),
    path('', views.main_home_page),
]
