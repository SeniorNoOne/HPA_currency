import django_filters

from currency.models import Rate, ContactUs, RequestResponseLog, Source


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'buy': ('lt', 'gt'),
            'sell': ('lt', 'gt'),
            'source__name': ('icontains',)
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'email_from': ('icontains',),
            'subject': ('icontains',),
            'message': ('icontains',)
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'url': ('icontains',),
            'name': ('icontains',),
            'city': ('icontains',)
        }


class RequestResponseLogFilter(django_filters.FilterSet):
    class Meta:
        model = RequestResponseLog
        fields = {
            'path': ('icontains',),
            'request_method': ('exact',),
            'time': ('lt', 'gt')
        }
