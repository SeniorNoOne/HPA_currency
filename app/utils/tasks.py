from django.core.mail import send_mail

from celery import shared_task

from utils.celery_classes import BaseTaskWithRetry


@shared_task(base=BaseTaskWithRetry)
def celery_send_mail(email):
    send_mail(**email)
