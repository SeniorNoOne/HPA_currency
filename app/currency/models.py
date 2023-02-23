from django.db import models


class Rate(models.Model):
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sell = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=25)
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

