from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from currency.constants import LATEST_RATE_CACHE_KEY
from currency.choices import RateCurrencyChoices
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

    @action(detail=False, methods=('GET',))
    def latest(self, request, *args, **kwargs):
        latest_rates = []
        if cached_rates := cache.get(LATEST_RATE_CACHE_KEY):
            return Response(cached_rates)

        for source_obj in Source.objects.all():
            for currency in RateCurrencyChoices:
                if latest := Rate.objects.filter(source=source_obj,
                                                 currency=currency).order_by('-created').first():
                    latest_rates.append(RateSerializer(instance=latest).data)

        cache.set(LATEST_RATE_CACHE_KEY, latest_rates, 60 * 60 * 24 * 7)
        return Response(latest_rates)


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
