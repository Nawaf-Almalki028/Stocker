from django.contrib import admin
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_home, name="dashboard_home"),
    path('suppliers/', views.dashboard_suppliers, name="dashboard_supplier"),
]
