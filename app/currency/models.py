from django.conf import settings
from django.db import models
from django.templatetags.static import static

from currency.choices import CurrencyInfoCurrencyChoices, RequestMethodChoices, \
    CurrencyInfoCurrencyMap

from phonenumber_field.modelfields import PhoneNumberField


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Buy')
    sell = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Sell')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    currency = models.ForeignKey('currency.CurrencyInfo', on_delete=models.CASCADE)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Currency: {self.buy}/{self.sell}'


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
    logo = models.ImageField(blank=True, null=True)

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


class CurrencyInfo(models.Model):
    code_name = models.PositiveSmallIntegerField(choices=CurrencyInfoCurrencyChoices.choices)
    full_name = models.CharField(max_length=64)
    icon_link = models.CharField(max_length=254)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.full_name, self.icon_link = CurrencyInfoCurrencyMap.get(self.code_name, ('', ''))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
