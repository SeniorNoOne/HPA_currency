from django.contrib import admin
from django.urls import path, include
from currency.views import MainPageView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    path('auth/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),

    path('', MainPageView.as_view(), name='index'),

    path('__debug__/', include('debug_toolbar.urls')),

    path('currency/', include('currency.urls'))
]
