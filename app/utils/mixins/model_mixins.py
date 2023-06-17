from django.conf import settings
from django.urls import reverse

from utils.tasks import celery_send_mail


class EmailBaseMixin:
    subject = ''
    from_email = settings.DEFAULT_FROM_EMAIL
    fail_silently = False

    def _create_email(self):
        pass

    @staticmethod
    def _send_email(email):
        # celery_send_mail.apply_async(args=[email], queue='mail')
        celery_send_mail(email)

    def send_email(self):
        email = self._create_email()
        self._send_email(email)


class SignUpEmailMixin(EmailBaseMixin):
    subject = 'Thank you for registration!'

    def _create_email(self):
        path = reverse('account:activate', args=(self.username,))
        message = 'To activate your account, follow the link:\n' + \
                  f'\n{settings.HTTP_SCHEMA}://{settings.HOST}{path}\n' + \
                  "\nSincerely, \nSupport Team"

        email = {'subject': self.subject,
                 'message': message,
                 'from_email': self.from_email,
                 'recipient_list': [self.email],
                 'fail_silently': False
                 }
        return email


class FeedbackEmailMixin(EmailBaseMixin):
    subject = 'User Feedback Form'

    def _create_email(self):
        message = f'Reply to email: {self.email_from}\n' + \
                  f'Subject: {self.subject}\n' + \
                  f'Body: {self.message}\n'

        email = {'subject': self.subject,
                 'message': message,
                 'from_email': self.email_from,
                 'recipient_list': [*settings.EMAIL_RECEIVER],
                 'fail_silently': False
                 }
        return email
