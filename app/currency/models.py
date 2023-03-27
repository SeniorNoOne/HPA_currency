from django.db import models

from currency.choices import RateCurrencyChoices, RequestMethodChoices

from phonenumber_field.modelfields import PhoneNumberField


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Buy')
    sell = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Sell')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    currency = models.PositiveSmallIntegerField(choices=RateCurrencyChoices.choices,
                                                default=RateCurrencyChoices.USD,
                                                verbose_name='Currency')
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE)

    def __str__(self):
        return f'Currency: {self.get_currency_display()} - {self.buy}/{self.sell}'


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    email_from = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f'Feedback from {self.email_from}'


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64, blank=True, default="")
    phone = PhoneNumberField(blank=True, unique=True, default="", null=True)

    def __str__(self):
        return self.name.capitalize()


class RequestResponseLog(models.Model):
    path = models.CharField(max_length=255)
    request_method = models.PositiveSmallIntegerField(choices=RequestMethodChoices.choices)
    time = models.PositiveSmallIntegerField()
