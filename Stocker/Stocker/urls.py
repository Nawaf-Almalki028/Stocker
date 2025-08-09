
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounting/', include("accounting.urls")),
    path('', include("main.urls")),
    path('dashboard/', include("dashboard.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
