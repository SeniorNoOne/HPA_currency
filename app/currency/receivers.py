from django.db.models.signals import pre_delete
from django.dispatch import receiver
from currency.models import Source
from utils.common import delete_dir
from currency.constants import StorageUniqueFields


@receiver(pre_delete, sender=Source)
def delete_content_dir(sender, instance, **kwargs):
    model_name = instance.__class__.__name__
    unique_val = str(getattr(instance, StorageUniqueFields.source))
    delete_dir(model_name, unique_val)
