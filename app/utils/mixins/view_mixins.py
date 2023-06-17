from urllib.parse import urlencode

from django.contrib.auth.mixins import UserPassesTestMixin


class SuperUserTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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
