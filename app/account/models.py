import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.templatetags.static import static

from account.constants import StorageUniqueFields
from utils.common import get_upload_to_path
from utils.mixins.model_mixins import SignUpEmailMixin


def user_upload_to(instance, filename):
    return get_upload_to_path(instance, StorageUniqueFields.user, filename)


class CustomUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        user = self.model(email=email, password=password, username=uuid.uuid4(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(SignUpEmailMixin, AbstractUser):
    avatar = models.ImageField(blank=True, null=True, upload_to=user_upload_to)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    # Fields required to create a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('images/account_avatar_default.png')
