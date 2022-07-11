from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

doc_patterns = [
    path('docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
