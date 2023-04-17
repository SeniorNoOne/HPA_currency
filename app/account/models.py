from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('account_avatar_default.png')
