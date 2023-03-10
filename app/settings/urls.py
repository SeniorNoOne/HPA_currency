from django.contrib import admin
from django.urls import path, include
from currency.views import MainPageView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    path('', MainPageView.as_view()),

    path('__debug__/', include('debug_toolbar.urls')),

    path('currency/', include('currency.urls'))
]
