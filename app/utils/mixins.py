from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.core.files.storage import default_storage

from utils.common import get_upload_to_path, get_instance_path
from utils.tasks import celery_send_mail, celery_save_file, celery_delete_file_dir


class CreateSignUpEmailMixin:
    @staticmethod
    def _create_email(instance):
        path = reverse('account:activate', args=(instance.username,))
        subject = 'Thank you for registration!'
        message = 'To activate your account, follow the link:\n' + \
                  f'\n{settings.HTTP_SCHEMA}://{settings.HOST}{path}\n' + \
                  "\nSincerely, \nSupport Team"

        email = {'subject': subject,
                 'message': message,
                 'from_email': settings.DEFAULT_FROM_EMAIL,
                 'recipient_list': [instance.email],
                 'fail_silently': False
                 }
        return email


class CreateFeedbackEmailMixin:
    @staticmethod
    def _create_email(instance):
        subject = 'User Feedback Form'
        message = f'Reply to email: {instance.email_from}\n' + \
                  f'Subject: {instance.subject}\n' + \
                  f'Body: {instance.message}\n'

        email = {'subject': subject,
                 'message': message,
                 'from_email': settings.DEFAULT_FROM_EMAIL,
                 'recipient_list': [*settings.EMAIL_RECEIVER],
                 'fail_silently': False
                 }
        return email


class SendMailMixin:
    @staticmethod
    def _send_mail(email):
        celery_send_mail.apply_async(args=[email], queue='mail')


class SendFeedbackMailMixin(CreateFeedbackEmailMixin, SendMailMixin):
    pass


class SendSignupMailMixin(CreateSignUpEmailMixin, SendMailMixin):
    pass


class SaveFileMixin:
    @staticmethod
    def _save_file(instance, target_field, unique_key):
        uploaded_file = getattr(instance, target_field)
        content = list(uploaded_file.read()) if uploaded_file else None
        if uploaded_file:
            path_to_file = get_upload_to_path(instance, uploaded_file.name, unique_key)
            celery_save_file.apply_async(args=[path_to_file, content, default_storage], queue='storage_tasks')
            # celery_save_file(path_to_file, content)
            setattr(instance, target_field, path_to_file)
        else:
            setattr(instance, target_field, None)
        # instance.save()


class DeleteFileMixin:
    @staticmethod
    def _delete_file_dir(instance, unique_key):
        path_to_instance = get_instance_path(instance, unique_key)
        celery_delete_file_dir.apply_async(args=[path_to_instance], queue='storage_tasks')


class SuperUserTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
