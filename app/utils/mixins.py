from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from utils.tasks import celery_send_mail, celery_save_file, celery_delete_file_dir


class CreateSignUpEmailMixin:
    def _create_email(self):
        path = reverse('account:activate', args=(self.object.username,))
        subject = 'Thank you for registration!'
        message = 'To activate your account, follow the link:\n' + \
                  f'\n{settings.HTTP_SCHEMA}://{settings.HOST}{path}\n' + \
                  "\nSincerely, \nSupport Team"

        email = {'subject': subject,
                 'message': message,
                 'from_email': settings.DEFAULT_FROM_EMAIL,
                 'recipient_list': [self.object.email],
                 'fail_silently': False
                 }
        return email


class CreateFeedbackEmailMixin:
    def _create_email(self):
        subject = 'User Feedback Form'
        message = f'Reply to email: {self.object.email_from}\n' + \
                  f'Subject: {self.object.subject}\n' + \
                  f'Body: {self.object.message}\n'

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
        # For Windows
        celery_send_mail(email)
        # UNIX
        # celery_send_mail.apply_async(args=[email], queue='mail')

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_mail(self._create_email())
        return redirect


class SuperUserTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SendFeedbackMailMixin(CreateFeedbackEmailMixin, SendMailMixin):
    pass


class SendSignupMailMixin(CreateSignUpEmailMixin, SendMailMixin):
    pass


class SaveFileMixin:
    def _save_file(self, form, target_field, unique_key):
        celery_save_file(form, target_field, unique_key)


class DeleteFileMixin:
    def _delete_file_dir(self, instance, unique_key, content):
        celery_delete_file_dir(instance, unique_key, content)
