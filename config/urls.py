from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse, HttpResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return JsonResponse({
        "message": "Django Auth API Running 🚀",
        "swagger": "/swagger/",
        "redoc": "/redoc/"
    })


def favicon(_request):
    return HttpResponse(status=204)

urlpatterns = [
    path('', home),
    path('favicon.ico', favicon),
    path('favicon.png', favicon),
    re_path(r'^favicon\.(ico|png)/?$', favicon),

    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema')),
]