from django.shortcuts import render
from currency.models import Rate, ContactUs


def show_currency_lst(request):
    result = Rate.objects.all()
    context = {'currency_lst': result}
    return render(request, 'currency.html', context)


def show_email_lst(request):
    result = ContactUs.objects.all()
    context = {'user_data': result}
    return render(request, 'contact_us.html', context)
