from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import path, include

from currency.views import MainPageView
from account.forms import CustomLoginForm, CustomResetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),

    path('auth/login/', LoginView.as_view(template_name='registration/login.html',
                                          authentication_form=CustomLoginForm),
         name='login'),

    path('auth/password_reset/',
         PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                   form_class=CustomResetPasswordForm),
         name='password_reset'),

    path('', MainPageView.as_view(), name='index'),

    path('account/', include('account.urls')),

    path('auth/', include('django.contrib.auth.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('currency/', include('currency.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
