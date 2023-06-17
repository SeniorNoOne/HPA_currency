from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from currency.constants import StorageUniqueFields, LATEST_RATE_CACHE_KEY
from currency.models import Source, Rate, ContactUs
from utils.common import delete_dir


@receiver(post_delete, sender=Source)
def source_delete_content_dir(sender, instance, **kwargs):
    delete_dir(instance, StorageUniqueFields.source)


@receiver(post_save, sender=Rate)
def rate_delete_cache_on_update(sender, instance, created, **kwargs):
    if created:
        cache.delete(LATEST_RATE_CACHE_KEY)


@receiver(post_save, sender=ContactUs)
def contact_us_send_feedback_mail(sender, instance, created, **kwargs):
    instance.send_email()
