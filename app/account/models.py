from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class User(AbstractUser):
    email = models.EmailField(unique=True)
    # upload_to parameter has been removed, but no new migration has been performed
    avatar = models.ImageField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('avatar_default.png')
