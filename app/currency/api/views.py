from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from currency.api.serializers import (RateSerializer, SourceSerializer,
                                      ContactUsSerializer, RequestResponseLogSerializer)
from currency.api.paginators import CurrencyApiLimitOffsetPagination
from currency.filters import RateFilter, SourceFilter, ContactUsFilter, RequestResponseLogFilter
from currency.models import Rate, Source, ContactUs, RequestResponseLog

from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters


# Did this in such way, since it does not work in settings.py
class CurrencyFilterBackendBase:
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter
    )


class RateApiViewSet(CurrencyFilterBackendBase, viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    filterset_class = RateFilter
    permission_classes = (AllowAny,)
    ordering_fields = ('id', 'buy', 'sell',)
    search_fields = ('source__name',)


class ContactUsApiViewSet(CurrencyFilterBackendBase, viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    filterset_class = ContactUsFilter
    ordering_fields = ('id', 'email_from', 'subject',)
    search_fields = ('email_from', 'subject', 'message',)


class SourceApiViewSet(CurrencyFilterBackendBase, viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    http_method_names = ('get',)
    filterset_class = SourceFilter
    ordering_fields = ('id', 'name', 'url',)
    search_fields = ('name', 'url', 'city',)


class RequestResponseLogApiViewSet(CurrencyFilterBackendBase, viewsets.ModelViewSet):
    queryset = RequestResponseLog.objects.all()
    serializer_class = RequestResponseLogSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    http_method_names = ('get', 'delete')
    filterset_class = RequestResponseLogFilter
    ordering_fields = ('id', 'path', 'time',)
    search_fields = ('path', 'request_method')
