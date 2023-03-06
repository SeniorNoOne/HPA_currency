from django.contrib import admin
from django.urls import path, include

from currency.views import (
    index,
    RateListView, RateDetailView, RateUpdateView, RateCreateView, RateDeleteView,
    contact_us_list, contact_us_details, contact_us_create,
    contact_us_update, contact_us_delete,
    source_list, source_details, source_create,
    source_update, source_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('__debug__/', include('debug_toolbar.urls')),

    path('', index),

    path('rate/create/', RateCreateView.as_view()),
    path('rate/list/', RateListView.as_view()),
    path('rate/details/<int:pk>/', RateDetailView.as_view()),
    path('rate/update/<int:pk>/', RateUpdateView.as_view()),
    path('rate/delete/<int:pk>/', RateDeleteView.as_view()),

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
