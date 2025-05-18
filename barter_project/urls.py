from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # встроенные URL-ы аутентификации (login, logout, password reset…)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('ads.urls')),
    path('api/', include('ads.api_urls')),
]
