from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
)

from currency.forms import ContactUsForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source, RequestResponseLog
from utils.mixins import SendFeedbackMailMixin, SuperUserTestMixin


class MainPageView(TemplateView):
    template_name = 'index.html'


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = 'rate/rate_create.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class RateListView(ListView):
    template_name = 'rate/rate_list.html'
    queryset = Rate.objects.select_related('source')  # prefetch_related(Prefetch('source'))


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


class ContactUsListView(ListView):
    template_name = 'contact_us/contact_us_list.html'
    queryset = ContactUs.objects.all()


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


class SourceCreateView(CreateView):
    form_class = SourceForm
    template_name = 'source/source_create.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')


class SourceListView(ListView):
    template_name = 'source/source_list.html'
    queryset = Source.objects.all()


class SourceDetailView(DetailView):
    template_name = 'source/source_details.html'
    queryset = Source.objects.all()


class SourceUpdateView(UpdateView):
    form_class = SourceForm
    template_name = 'source/source_update.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')


class SourceDeleteView(DeleteView):
    template_name = 'source/source_delete.html'
    queryset = Source.objects.all()
    success_url = reverse_lazy('currency:source-list')


class LogListView(ListView):
    template_name = 'log/log_list.html'
    queryset = RequestResponseLog.objects.all()
