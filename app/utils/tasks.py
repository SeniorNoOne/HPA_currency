from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail

from celery import shared_task

from utils.common import get_upload_to_path, get_instance_path
from utils.celery_classes import BaseTaskWithRetry


@shared_task(base=BaseTaskWithRetry)
def celery_send_mail(email):
    send_mail(**email)


@shared_task(base=BaseTaskWithRetry)
def celery_save_file(form, target_field, unique_key):
    uploaded_file = form.cleaned_data[target_field]
    content = uploaded_file.read() if uploaded_file else None
    instance = form.save(commit=False)

    if uploaded_file:
        path_to_file = get_upload_to_path(instance, uploaded_file.name, unique_key)

        if not default_storage.exists(path_to_file):
            filename = default_storage.save(path_to_file, ContentFile(content))
            instance.logo = filename
    else:
        instance.logo = None
    instance.save()


@shared_task(base=BaseTaskWithRetry)
def celery_delete_file_dir(instance, unique_key):
    dir_path = get_instance_path(instance, unique_key)
    default_storage.delete(dir_path)
