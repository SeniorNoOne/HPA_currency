from django.core.cache import cache

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from currency.filters import ContactUsFilter, RateFilter, RequestResponseLogFilter, SourceFilter
from currency.api.paginators import CurrencyApiCursorPagination
from currency.api.serializers import (ContactUsSerializer,
                                      RateSerializer,
                                      RequestResponseLogSerializer,
                                      SourceSerializer)
from currency.api.throttling import CurrencyAnonThrottle, CurrencyUserThrottle
from currency.choices import RateCurrencyChoices
from currency.constants import LATEST_RATE_CACHE_KEY
from currency.models import ContactUs, Rate, RequestResponseLog, Source


class RateApiViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filterset_class = RateFilter
    pagination_class = CurrencyApiCursorPagination
    permission_classes = (AllowAny,)
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]

    ordering = ('-id',)
    ordering_fields = ('id', 'buy', 'sell',)
    search_fields = ('source__name',)

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
    filterset_class = ContactUsFilter
    pagination_class = CurrencyApiCursorPagination
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]

    ordering = ('-id',)
    ordering_fields = ('id', 'email_from', 'subject',)
    search_fields = ('email_from', 'subject', 'message',)


class SourceApiViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    pagination_class = CurrencyApiCursorPagination
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]

    ordering = ('-id',)
    ordering_fields = ('id', 'name', 'url',)
    search_fields = ('name', 'url', 'city',)


class RequestResponseLogApiViewSet(mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    queryset = RequestResponseLog.objects.all()
    serializer_class = RequestResponseLogSerializer
    filterset_class = RequestResponseLogFilter
    pagination_class = CurrencyApiCursorPagination
    throttle_classes = [CurrencyAnonThrottle, CurrencyUserThrottle]

    ordering = ('-id',)
    ordering_fields = ('id', 'path', 'time',)
    search_fields = ('path', 'request_method',)
