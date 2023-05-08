from django.conf import settings
from django.db import models
from django.templatetags.static import static

from currency.choices import RateCurrencyChoices, RequestMethodChoices
from utils.common import upload_to_path
from currency.constants import StorageUniqueFields

from phonenumber_field.modelfields import PhoneNumberField


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Buy')
    sell = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Sell')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    currency = models.PositiveSmallIntegerField(choices=RateCurrencyChoices.choices,
                                                default=RateCurrencyChoices.USD,
                                                verbose_name='Currency')
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Currency: {self.get_currency_display()} - {self.buy}/{self.sell}'


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email_from = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f'Feedback from {self.email_from}'


class Source(models.Model):
    url = models.CharField(max_length=255)
    code = models.SmallIntegerField(unique=True)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64, blank=True)
    phone = PhoneNumberField(blank=True, unique=True, null=True)
    logo = models.ImageField(blank=True, null=True,
                             upload_to=upload_to_path(StorageUniqueFields.source))

    def __str__(self):
        return self.name.capitalize()

    @property
    def logo_url(self):
        if self.logo:
            if settings.STATIC_URL in str(self.logo):
                return str(self.logo)
            else:
                return self.logo.url
        return static('source_logo_default.png')


class RequestResponseLog(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.PositiveSmallIntegerField(choices=RequestMethodChoices.choices)
    time = models.PositiveSmallIntegerField()
