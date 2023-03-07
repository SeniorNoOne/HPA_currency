from django.urls import path

from currency.views import (
    RateListView, RateDetailView, RateUpdateView, RateCreateView, RateDeleteView,
    ContactUsCreateView, ContactUsListView, ContactUsDetailView, ContactUsUpdateView,
    ContactUsDeleteView,
    SourceCreateView, SourceListView, SourceDetailView, SourceUpdateView, SourceDeleteView
)

app_name = 'currency'

urlpatterns = [
    path('rate/create/', RateCreateView.as_view(), name='rate-create'),
    path('rate/list/', RateListView.as_view(), name='rate-list'),
    path('rate/details/<int:pk>/', RateDetailView.as_view(), name='rate-details'),
    path('rate/update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),
    path('rate/delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),

    path('contact_us/create/', ContactUsCreateView.as_view(), name='contactus-create'),
    path('contact_us/list/', ContactUsListView.as_view(), name='contactus-list'),
    path('contact_us/details/<int:pk>/', ContactUsDetailView.as_view(), name='contactus-details'),
    path('contact_us/update/<int:pk>/', ContactUsUpdateView.as_view(), name='contactus-update'),
    path('contact_us/delete/<int:pk>/', ContactUsDeleteView.as_view(), name='contactus-delete'),

    path('source/create/', SourceCreateView.as_view(), name='source-create'),
    path('source/list/', SourceListView.as_view(), name='source-list'),
    path('source/details/<int:pk>/', SourceDetailView.as_view(), name='source-details'),
    path('source/update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),
]
