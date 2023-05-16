from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from currency.models import Source, Rate
from utils.common import delete_dir
from currency.constants import StorageUniqueFields, LATEST_RATE_CACHE_KEY


@receiver(post_delete, sender=Source)
def delete_source_content_dir(sender, instance, **kwargs):
    delete_dir(instance, StorageUniqueFields.source)


@receiver(post_save, sender=Rate)
def delete_cache_on_rate_update(sender, instance, created, **kwargs):
    if created:
        cache.delete(LATEST_RATE_CACHE_KEY)
