from django.core.management.base import BaseCommand
from currency.models import Source


class Command(BaseCommand):
    help = "Deletes random testing rates and corresponding source"

    def handle(self, *args, **options):
        source_kwargs = {
            'url': 'test/url',
            'code': -1,
            'name': 'test_source',
        }

        Source.objects.filter(code=source_kwargs['code']).delete()
