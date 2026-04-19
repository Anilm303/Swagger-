from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

def home(request):
    return JsonResponse({
        "message": "Django Auth API Running 🚀",
        "swagger": "/swagger/",
        "redoc": "/redoc/"
    })

schema_view = get_schema_view(
    openapi.Info(
        title="Django Auth API",
        default_version='v1',
        description="JWT Auth API with Swagger",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger.json', schema_view.without_ui(cache_timeout=0)),
]