from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
)

from currency.forms import ContactUsForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source, RequestResponseLog
from currency.filters import RateFilter, RequestResponseLogFilter, ContactUsFilter
from utils.mixins import (
    SendFeedbackMailMixin, SuperUserTestMixin, SaveFileMixin, DeleteFileMixin, CustomPaginationMixin
)

from django_filters.views import FilterView


class MainPageView(TemplateView):
    template_name = 'index.html'


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = 'rate/rate_create.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class RateListView(CustomPaginationMixin, FilterView):
    template_name = 'rate/rate_list.html'
    queryset = Rate.objects.select_related('source')  # prefetch_related(Prefetch('source'))
    filterset_class = RateFilter


class RateDetailView(LoginRequiredMixin, DetailView):
    template_name = 'rate/rate_details.html'
    queryset = Rate.objects.all()


class RateUpdateView(SuperUserTestMixin, UpdateView):
    form_class = RateForm
    template_name = 'rate/rate_update.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class RateDeleteView(SuperUserTestMixin, DeleteView):
    template_name = 'rate/rate_delete.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class ContactUsCreateView(SendFeedbackMailMixin, CreateView):
    form_class = ContactUsForm
    template_name = 'contact_us/contact_us_create.html'
    queryset = ContactUs.objects.all()
    success_url = reverse_lazy('currency:contactus-list')


class ContactUsListView(CustomPaginationMixin, FilterView):
    template_name = 'contact_us/contact_us_list.html'
    queryset = ContactUs.objects.all()
    filterset_class = ContactUsFilter


class ContactUsDetailView(DetailView):
    template_name = 'contact_us/contact_us_details.html'
    queryset = ContactUs.objects.all()


class ContactUsUpdateView(SendFeedbackMailMixin, UpdateView):
    form_class = ContactUsForm
    template_name = 'contact_us/contact_us_update.html'
    queryset = ContactUs.objects.all()
    success_url = reverse_lazy('currency:contactus-list')


class ContactUsDeleteView(DeleteView):
    template_name = 'contact_us/contact_us_delete.html'
    queryset = ContactUs.objects.all()
    success_url = reverse_lazy('currency:contactus-list')


class SourceCreateView(CreateView, SaveFileMixin):
    form_class = SourceForm
    template_name = 'source/source_create.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        self._save_file(cleaned_data, 'source', 'logo', 'code')
        return super().form_valid(form)


class SourceListView(ListView):
    template_name = 'source/source_list.html'
    queryset = Source.objects.all()


class SourceDetailView(DetailView):
    template_name = 'source/source_details.html'
    queryset = Source.objects.all()


class SourceUpdateView(UpdateView, SaveFileMixin):
    form_class = SourceForm
    template_name = 'source/source_update.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        self._save_file(cleaned_data, 'source', 'logo', 'code')
        return super().form_valid(form)


class SourceDeleteView(DeleteView, DeleteFileMixin):
    template_name = 'source/source_delete.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')

    def form_valid(self, form):
        instance = self.get_object()
        self._delete_file_dir(instance, 'code')
        return super().form_valid(form)


class LogListView(CustomPaginationMixin, FilterView):
    template_name = 'log/log_list.html'
    queryset = RequestResponseLog.objects.all()
    filterset_class = RequestResponseLogFilter
