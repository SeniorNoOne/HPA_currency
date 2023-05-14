from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static

from utils.common import get_upload_to_path
from account.constants import StorageUniqueFields


def user_upload_to(instance, filename):
    return get_upload_to_path(instance, StorageUniqueFields.user, filename)


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_upload_to)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('account_avatar_default.png')
