import django_filters
from django.forms import NumberInput, Select, TextInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row

from currency.models import Rate, ContactUs, RequestResponseLog, Source
from currency.constants import RATE_FILTER_LOOKUPS


class RateFilter(django_filters.FilterSet):
    buy__lookup = django_filters.ChoiceFilter(
        label='Buy filter',
        widget=Select(attrs={'class': 'form-control'}),
        choices=RATE_FILTER_LOOKUPS['buy'],
    )
    buy = django_filters.NumberFilter(
        field_name='buy',
        widget=NumberInput(attrs={'class': 'form-control'}),
    )

    sell__lookup = django_filters.ChoiceFilter(
        label='Sell filter',
        widget=Select(attrs={'class': 'form-control'}),
        choices=RATE_FILTER_LOOKUPS['sell'],
    )
    sell = django_filters.NumberFilter(
        field_name='sell',
        widget=NumberInput(attrs={'class': 'form-control'}),
    )

    source__name__lookup = django_filters.ChoiceFilter(
        label='Source filter',
        widget=Select(attrs={'class': 'form-control'}),
        choices=RATE_FILTER_LOOKUPS['source__name'],
    )
    source__name = django_filters.CharFilter(
        field_name='source__name',
        widget=TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Rate
        fields = []

    def filter_queryset(self, queryset):
        # queryset = super().filter_queryset(queryset)

        for field in RATE_FILTER_LOOKUPS['filter_fields']:
            lookup_expr = self.form.cleaned_data.get(f'{field}__lookup', None)
            filter_value = self.form.cleaned_data.get(f'{field}', None)

            if lookup_expr and filter_value is not None:
                queryset = queryset.filter(**{f'{field}__{lookup_expr}': filter_value})
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('buy__lookup', 'buy', css_class='col-8 mt-3'),
            ),
            Row(
                Column('sell__lookup', 'sell', css_class='col-8 mt-3'),
            ),
            Row(
                Column('source__name__lookup', 'source__name', css_class='col-8 mt-3'),
                css_class='collapse mt-4',
                id='collapseFilter'
            )
        )


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
