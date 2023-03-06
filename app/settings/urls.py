from django.contrib import admin
from django.urls import path

from currency.views import (
    index,
    rate_list, rate_details, rate_create, rate_update, rate_delete,
    contact_us_list, contact_us_details, contact_us_create,
    contact_us_update, contact_us_delete,
    source_list, source_details, source_create,
    source_update, source_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),

    path('rate/create/', rate_create),
    path('rate/list/', rate_list),
    path('rate/details/<int:pk>/', rate_details),
    path('rate/update/<int:pk>/', rate_update),
    path('rate/delete/<int:pk>/', rate_delete),

    path('contact_us/create/', contact_us_create),
    path('contact_us/list/', contact_us_list),
    path('contact_us/details/<int:pk>/', contact_us_details),
    path('contact_us/update/<int:pk>/', contact_us_update),
    path('contact_us/delete/<int:pk>/', contact_us_delete),

    path('source/create/', source_create),
    path('source/list/', source_list),
    path('source/details/<int:pk>/', source_details),
    path('source/update/<int:pk>/', source_update),
    path('source/delete/<int:pk>/', source_delete),
]
