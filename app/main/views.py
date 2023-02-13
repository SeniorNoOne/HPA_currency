from django.shortcuts import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse('Hello World!')
