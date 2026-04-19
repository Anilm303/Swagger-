from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return JsonResponse({
        "message": "Django Auth API Running 🚀",
        "swagger": "/swagger/",
        "redoc": "/redoc/"
    })

urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema')),
]