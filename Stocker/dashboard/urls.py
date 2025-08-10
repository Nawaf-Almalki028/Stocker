from django.contrib import admin
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_home, name="dashboard_home"),
    path('products/', views.dashboard_prod, name="dashboard_prod"),
    path('suppliers/', views.dashboard_suppliers, name="dashboard_supplier"),
    path('categories/', views.dashboard_categ, name="dashboard_categ"),
]
