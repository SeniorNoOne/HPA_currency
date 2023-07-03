import django_filters

from currency.models import Rate, ContactUs, RequestResponseLog, Source
from currency.constants import RateFilterConfig
from currency.forms import RateFilterForm


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = RateFilterConfig.filter_fields
        form = RateFilterForm

    def filter_queryset(self, queryset):
        for field in RateFilterConfig.filter_fields:
            lookup_expr = self.form.cleaned_data.get(f'{field}__lookup', None)
            filter_value = self.form.cleaned_data.get(f'{field}', None)

            if lookup_expr and filter_value:
                queryset = queryset.filter(**{f'{field}__{lookup_expr}': filter_value})

        return queryset


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'email_from': ('icontains',),
            'subject': ('icontains',),
            'message': ('icontains',),
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'url': ('icontains',),
            'name': ('icontains',),
            'city': ('icontains',),
        }


class RequestResponseLogFilter(django_filters.FilterSet):
    class Meta:
        model = RequestResponseLog
        fields = {
            'path': ('icontains',),
            'request_method': ('exact',),
            'time': ('exact', 'lt', 'lte', 'gt', 'gte',),
        }
