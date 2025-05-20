from django.contrib import admin
from django.urls import path, include
from ads.views import SignUpView, ProfileView, ProfileUpdateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # встроенные URL-ы аутентификации (login, logout, password reset…)
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path("accounts/profile/", ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path('', include('ads.urls')),
    path('api/', include('ads.api_urls')),
    # OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

