from django.contrib import admin
from django.urls import path, include

from currency.views import (
    index,

    RateListView, RateDetailView, RateUpdateView, RateCreateView, RateDeleteView,

    ContactUsCreateView, ContactUsListView, ContactUsDetailView, ContactUsUpdateView,
    ContactUsDeleteView,

    SourceCreateView, SourceListView, SourceDetailView, SourceUpdateView, SourceDeleteView
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

    path('contact_us/create/', ContactUsCreateView.as_view()),
    path('contact_us/list/', ContactUsListView.as_view()),
    path('contact_us/details/<int:pk>/', ContactUsDetailView.as_view()),
    path('contact_us/update/<int:pk>/', ContactUsUpdateView.as_view()),
    path('contact_us/delete/<int:pk>/', ContactUsDeleteView.as_view()),

    path('source/create/', SourceCreateView.as_view()),
    path('source/list/', SourceListView.as_view()),
    path('source/details/<int:pk>/', SourceDetailView.as_view()),
    path('source/update/<int:pk>/', SourceUpdateView.as_view()),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view()),
]
