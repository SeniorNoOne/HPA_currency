from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from account.constants import StorageUniqueFields
from utils.common import delete_dir

User = get_user_model()


@receiver(pre_save, sender=User)
def user_lower_email(sender, instance, **kwargs):
    instance.email = instance.email.lower()


@receiver(pre_save, sender=User)
def user_clean_phone(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join(token for token in instance.phone if token.isdigit())


@receiver(post_delete, sender=User)
def user_delete_content_dir(sender, instance, **kwargs):
    delete_dir(instance, StorageUniqueFields.user)


@receiver(post_save, sender=User)
def user_send_sing_up_email(sender, instance, created, **kwargs):
    if created:
        instance.send_email()
