from django.contrib import admin

from import_export.admin import ExportMixin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter

from currency.models import ContactUs, Rate, Source


@admin.register(Rate)
class RateAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'buy', 'sell', 'currency', 'source', 'created')
    list_filter = (
        'currency',
        ('buy', NumericRangeFilter),
        ('sell', NumericRangeFilter),
        ('created', DateRangeFilter),
    )
    search_fields = ('source', 'buy', 'sell',)


@admin.register(ContactUs)
class ContactUs(admin.ModelAdmin):
    list_display = ('id', 'email_from', 'subject', 'message',)
    search_fields = ('email_from', 'subject',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'name', 'city_display', 'phone',)
    search_fields = ('name', 'city', 'phone',)

    def city_display(self, obj):
        return obj.city or '-'

    city_display.short_description = 'City'
