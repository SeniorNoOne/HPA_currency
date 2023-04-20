from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from account.forms import CustomLoginForm
from currency.views import MainPageView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    path('auth/login/', LoginView.as_view(template_name='registration/login.html',
                                          authentication_form=CustomLoginForm),
         name='login'),

    path('', MainPageView.as_view(), name='index'),

    path('account/', include('account.urls')),

    path('auth/', include('django.contrib.auth.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('currency/', include('currency.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
