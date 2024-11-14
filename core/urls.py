from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Advokat Uz Api",
      default_version='v1',
      description="Bu yerdan Advokat Uz mobile app uchun apilar bor ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="xolqiberdiyevbehruz12@gmail.com"),
      license=openapi.License(name="Advokat Uz"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # apps
    path('api/v1/accounts/', include('accounts.urls')),
    path('common/', include('common.urls')),
    # swagger and redoc
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path('set_language/', include('django.conf.urls.i18n')),
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)