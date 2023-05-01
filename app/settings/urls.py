from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.forms import CustomLoginForm
from currency.views import MainPageView


schema_view = get_schema_view(
   openapi.Info(
      title="Currency API",
      default_version='v1',
      description="Basic documentation of Currency API",
      terms_of_service="http://127.0.0.1:8000/",
      contact=openapi.Contact(url="http://127.0.0.1:8000/"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    path('auth/login/', LoginView.as_view(template_name='registration/login.html',
                                          authentication_form=CustomLoginForm),
         name='login'),

    path('', MainPageView.as_view(), name='index'),

    path('account/', include('account.urls')),

    path('auth/', include('django.contrib.auth.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('currency/', include('currency.urls')),

    path('api/', include('account.api.urls')),
    path('api/currency/', include('currency.api.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'
            ),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
            ),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'
            ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
