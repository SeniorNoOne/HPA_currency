from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail

from celery import shared_task

from utils.celery_classes import BaseTaskWithRetry


@shared_task(base=BaseTaskWithRetry)
def celery_send_mail(email):
    send_mail(**email)


@shared_task(base=BaseTaskWithRetry)
def celery_save_file(path_to_file, content, storage):
    print(storage.__class__.__name__)
    content = bytes(content)
    a = storage.save(path_to_file, ContentFile(content))
    print(a)
    return a
    # if not default_storage.exists(path_to_file):


@shared_task(base=BaseTaskWithRetry)
def celery_delete_file_dir(path_to_instance):
    if default_storage.exists(path_to_instance):
        for file_name in default_storage.listdir(path_to_instance)[1]:
            file_path = f"{path_to_instance}/{file_name}"
            default_storage.delete(file_path)
        default_storage.delete(path_to_instance)
