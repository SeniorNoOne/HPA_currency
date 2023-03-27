from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse


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
    def _send_mail(self, email):
        send_mail(**email)

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
