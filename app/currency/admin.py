from django.contrib import admin
from currency.models import Rate

from rangefilter.filters import DateRangeFilter, NumericRangeFilter
from import_export.admin import ExportMixin


@admin.register(Rate)
class RateAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'buy', 'sell', 'currency', 'source', 'created')
    list_filter = (
        'currency',
        ('buy', NumericRangeFilter),
        ('sell', NumericRangeFilter),
        ('created', DateRangeFilter)
    )
    search_fields = ('source', 'buy', 'sell')
