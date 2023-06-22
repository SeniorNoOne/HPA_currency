from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static

from account.constants import StorageUniqueFields
from utils.common import get_upload_to_path
from utils.mixins.model_mixins import SignUpEmailMixin


def user_upload_to(instance, filename):
    return get_upload_to_path(instance, StorageUniqueFields.user, filename)


class User(SignUpEmailMixin, AbstractUser):
    # Fields required to create a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    avatar = models.ImageField(blank=True, null=True, upload_to=user_upload_to)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('images/account_avatar_default.png')
