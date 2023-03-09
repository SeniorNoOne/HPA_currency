from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from currency.choices import RateCurrencyChoices


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency = models.PositiveSmallIntegerField(choices=RateCurrencyChoices.choices,
                                                default=RateCurrencyChoices.USD)
    source = models.CharField(max_length=25)

    def __str__(self):
        str_repr = ""
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                str_repr += f"{key}: {value}; "
        return str_repr


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        str_repr = ""
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                str_repr += f"{key}: {value}; "
        return str_repr


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64, blank=True, default="")
    phone = PhoneNumberField(blank=True, unique=True, default="", null=True)

    def __str__(self):
        str_repr = ""
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                str_repr += f"{key}: {value}; "
        return str_repr
