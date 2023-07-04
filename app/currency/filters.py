import django_filters

from currency.constants import RateFilterConfig, ContactUsFilterConfig, SourceFilterConfig, \
    RequestResponseLogFilterConfig
from currency.forms import RateFilterForm, ContactUsFilterForm, SourceFilterForm, \
    RequestResponseLogFilterForm
from currency.models import Rate, ContactUs, RequestResponseLog, Source


class BaseFilter(django_filters.FilterSet):
    filter_config = None

    def filter_queryset(self, queryset):
        for field in self.filter_config.filter_fields:
            lookup_expr = self.form.cleaned_data.get(f'{field}_lookup', None)
            filter_value = self.form.cleaned_data.get(f'{field}', None)

            if lookup_expr and filter_value:
                queryset = queryset.filter(**{f'{field}__{lookup_expr}': filter_value})

        return queryset


class RateFilter(BaseFilter):
    class Meta:
        model = Rate
        fields = ()
        form = RateFilterForm

    filter_config = RateFilterConfig


class ContactUsFilter(BaseFilter):
    class Meta:
        model = ContactUs
        fields = ()
        form = ContactUsFilterForm

    filter_config = ContactUsFilterConfig


class SourceFilter(BaseFilter):
    class Meta:
        model = Source
        fields = ()
        form = SourceFilterForm

    filter_config = SourceFilterConfig


class RequestResponseLogFilter(BaseFilter):
    class Meta:
        model = RequestResponseLog
        fields = ()
        form = RequestResponseLogFilterForm

    filter_config = RequestResponseLogFilterConfig
