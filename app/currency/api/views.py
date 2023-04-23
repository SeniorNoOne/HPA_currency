from rest_framework import viewsets

from currency.api.serializers import (RateSerializer, SourceSerializer,
                                      ContactUsSerializer, RequestResponseLogSerializer)
from currency.models import Rate, Source, ContactUs, RequestResponseLog


class RateApiViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class SourceApiViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactUsApiViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    http_method_names = ('get', 'post', 'delete')


class RequestResponseLogApiViewSet(viewsets.ModelViewSet):
    queryset = RequestResponseLog.objects.all()
    serializer_class = RequestResponseLogSerializer
    http_method_names = ('get', 'delete')
