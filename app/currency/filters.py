import django_filters

from currency.models import Rate, ContactUs, RequestResponseLog


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = ('buy', 'sell')


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = ('email_from', 'subject')


class RequestResponseLogFilter(django_filters.FilterSet):
    class Meta:
        model = RequestResponseLog
        fields = ('path', 'request_method', 'time')
