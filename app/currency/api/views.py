from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from currency.api.paginators import CurrencyApiLimitOffsetPagination
from currency.api.serializers import (RateSerializer, SourceSerializer,
                                      ContactUsSerializer, RequestResponseLogSerializer)
from currency.api.throttling import CurrencyAnonThrottle, CurrencyUserThrottle
from currency.filters import RateFilter, SourceFilter, ContactUsFilter, RequestResponseLogFilter
from currency.models import Rate, Source, ContactUs, RequestResponseLog


class RateApiViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    filterset_class = RateFilter
    permission_classes = (AllowAny,)
    ordering_fields = ('id', 'buy', 'sell',)
    search_fields = ('source__name',)
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]


class ContactUsApiViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    filterset_class = ContactUsFilter
    ordering_fields = ('id', 'email_from', 'subject',)
    search_fields = ('email_from', 'subject', 'message',)
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]


class SourceApiViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    http_method_names = ('get',)
    filterset_class = SourceFilter
    ordering_fields = ('id', 'name', 'url',)
    search_fields = ('name', 'url', 'city',)
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]


class RequestResponseLogApiViewSet(viewsets.ModelViewSet):
    queryset = RequestResponseLog.objects.all()
    serializer_class = RequestResponseLogSerializer
    pagination_class = CurrencyApiLimitOffsetPagination
    http_method_names = ('get', 'delete')
    filterset_class = RequestResponseLogFilter
    ordering_fields = ('id', 'path', 'time',)
    search_fields = ('path', 'request_method')
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]
