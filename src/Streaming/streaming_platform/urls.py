#streaming_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
   SpectacularAPIView,
   SpectacularSwaggerView,
   SpectacularRedocView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Suas outras URLs
    path('admin/', admin.site.urls),
    path('api/', include('content_app.urls')),  # Inclua as URLs do seu app
    path('api/token/', obtain_auth_token, name='api_token_auth'),

   # Schema OpenAPI
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

   # UIs de documentação
   path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]