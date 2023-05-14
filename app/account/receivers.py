from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from account.constants import StorageUniqueFields
from utils.common import delete_dir

User = get_user_model()


@receiver(pre_save, sender=User)
def user_lower_email(sender, instance, **kwargs):
    if instance.email:
        email = instance.email.lower()
        if User.objects.filter(email=email).exclude(pk=instance.pk).exists():
            raise ValidationError('Email address must be unique')
        else:
            instance.email = email


@receiver(pre_save, sender=User)
def user_clean_phone(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join(token for token in instance.phone if token.isdigit())


@receiver(pre_delete, sender=User)
def delete_content_dir(sender, instance, **kwargs):
    delete_dir(instance, StorageUniqueFields.user)
