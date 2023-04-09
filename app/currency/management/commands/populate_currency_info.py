from django.core.management.base import BaseCommand
from currency.models import CurrencyInfo, CurrencyInfoCurrencyChoices


class Command(BaseCommand):
    _help = 'Populates CurrencyInfo model with initial data'

    def handle(self, *args, **options):
        for code, name in CurrencyInfoCurrencyChoices.choices:
            CurrencyInfo.objects.get_or_create(
                code_name=code,
            )
        self.stdout.write(self.style.SUCCESS('CurrencyInfo data populated successfully.'))
