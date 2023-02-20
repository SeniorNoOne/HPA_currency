from django.shortcuts import render
from django.http import HttpResponse

from currency.models import Rate, ContactUs


def show_currency_lst(request):
    result = [str(querry) for querry in Rate.objects.all()]
    if not result:
        result = ["No records in CURRENCY_RATE database"]
    return HttpResponse("<br>".join(result))


def show_email_lst(request):
    result = [str(querry) for querry in ContactUs.objects.all()]
    if not result:
        result = ["No records in CURRENCY_CONTACTUS database"]
    return HttpResponse("<br>".join(result))

