import random

from django.core.management.base import BaseCommand
from currency.models import Rate, Source
from currency.choices import RateCurrencyChoices


class Command(BaseCommand):
    help = "Generates random testing rates and corresponding source"

    def handle(self, *args, **options):
        source_kwargs = {
            'url': 'test/url',
            'code': -1,
            'name': 'test_source',
        }

        test_source, _ = Source.objects.get_or_create(code=source_kwargs['code'],
                                                      defaults=source_kwargs)

        for _ in range(300):
            Rate.objects.create(
                buy=random.randint(10, 30),
                sell=random.randint(10, 30),
                currency=random.choices(RateCurrencyChoices.choices)[0][0],
                source=test_source
            )
