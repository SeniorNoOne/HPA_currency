from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from utils.helpers import get_upload_to_path


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=get_upload_to_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('avatar_default.png')
