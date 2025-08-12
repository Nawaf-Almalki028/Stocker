from django.contrib import admin
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard_home, name="dashboard_home"),
    path('products/', views.dashboard_prod, name="dashboard_prod"),
    path('products/edit/<int:product_id>', views.dashboard_prod_edit, name="dashboard_prod_edit"),
    path('products/view/<int:product_id>', views.dashboard_prod_view, name="dashboard_prod_view"),
    path('products/delete/<int:product_id>', views.dashboard_prod_delete, name="dashboard_prod_delete"),
    path('suppliers/', views.dashboard_suppliers, name="dashboard_supplier"),
    path('suppliers/edit/<int:supplier_id>', views.dashboard_supplier_edit, name="dashboard_supplier_edit"),
    path('suppliers/delete/<int:supplier_id>', views.dashboard_supplier_delete, name="dashboard_supplier_delete"),
    path('suppliers/view/<int:supplier_id>', views.dashboard_supplier_view, name="dashboard_supplier_view"),
    path('stock/', views.dashboard_stock, name="dashboard_stock"),
    path('reports/', views.dashboard_reports, name="dashboard_reports"),
    path('categories/', views.dashboard_categ, name="dashboard_categ"),
    path('categories/delete/<int:catg_id>', views.dashboard_categ_delete, name="dashboard_categ_delete"),
    path('categories/edit/<int:catg_id>', views.dashboard_categ_edit, name="dashboard_categ_edit"),
    path('search/', views.search_results, name='search_results'),
    
]
