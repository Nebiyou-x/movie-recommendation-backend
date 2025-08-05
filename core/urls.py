from django.contrib import admin
from django.urls import path, re_path, include
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path


# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="API documentation for the Movie Recommendation App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view.security_definitions = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

urlpatterns = [
    # Redirect root to Swagger UI
    path('', lambda request: HttpResponseRedirect('/api/docs/')),

    # Admin
    path('admin/', admin.site.urls),

    # Swagger docs
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Movies API
    path('api/movies/', include('movies.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Django Auth URLs for Swagger login
    path('accounts/', include('django.contrib.auth.urls')),
]



# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
