from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.files.storage import default_storage

from utils.common import get_upload_to_path, get_instance_path
from utils.tasks import celery_send_mail


class GetValByNameMixin:
    @staticmethod
    def get_val(obj, var_name):
        """
        This method is needed to ensure that _create_mail method
        will work with both - instances of classes and dicts
        """
        if isinstance(obj, dict):
            return obj.get(var_name)
        else:
            return getattr(obj, var_name)


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


class CreateFeedbackEmailMixin(GetValByNameMixin):
    def _create_email(self, instance):
        subject = 'User Feedback Form'
        message = f'Reply to email: {self.get_val(instance, "email_from")}\n' + \
                  f'Subject: {self.get_val(instance, "subject")}\n' + \
                  f'Body: {self.get_val(instance, "message")}\n'

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
    def _save_file(cleaned_data, model_name, file_field_name, unique_field_name):
        model_name = model_name.lower()
        uploaded_file = cleaned_data.get(file_field_name)
        unique_key = str(cleaned_data.get(unique_field_name, 'lost_dir'))
        content = ContentFile(uploaded_file.read()) if uploaded_file else None
        if uploaded_file:
            path_to_file = get_upload_to_path(model_name, unique_key, uploaded_file.name)
            if not default_storage.exists(path_to_file):
                path_to_file = default_storage.save(path_to_file, content)
        else:
            path_to_file = None
        return path_to_file


class DeleteFileMixin:
    @staticmethod
    def _delete_file_dir(instance, unique_field_name):
        model_name = instance.__class__.__name__.lower()
        unique_key = str(getattr(instance, unique_field_name))
        path_to_instance = get_instance_path(model_name, unique_key)
        if dirs := default_storage.listdir(path_to_instance):
            for file_name in dirs[1]:
                file_path = f"{path_to_instance}/{file_name}"
                default_storage.delete(file_path)
            default_storage.delete(path_to_instance)


class SuperUserTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class PreserveQueryParamsMixin:
    pass


class CustomPaginationMixin:
    paginate_by = 20

    @staticmethod
    def _get_filter_params(request):
        filter_params = request.GET.dict()
        filter_params.pop('page', None)
        return urlencode(filter_params)

    def get_context_data(self, **kwargs):
        filter_params = self._get_filter_params(self.request)
        context = super().get_context_data(**kwargs)
        context['filter_params'] = filter_params
        return context
