from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('api/', include('ads.api_urls')),
]
