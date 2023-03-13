from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
)
from currency.forms import ContactUsForm, RateForm, SourceForm
from currency.models import ContactUs, Rate, Source, RequestResponseLog
from django.core.mail import send_mail
from django.conf import settings


class SendMessageMixin:
    def _send_mail(self):
        subject = 'User Feedback Form'
        message = f'Reply to email: {self.object.email_from}\n' + \
                  f'Subject: {self.object.subject}\n' + \
                  f'Body: {self.object.message}\n'
        send_mail(subject, message, settings.EMAIL_SENDER, [*settings.EMAIL_RECEIVER],
                  fail_silently=False)

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_mail()
        return redirect


class MainPageView(TemplateView):
    template_name = 'index.html'


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = 'rate/rate_create.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class RateListView(ListView):
    template_name = 'rate/rate_list.html'
    queryset = Rate.objects.all()


class RateDetailView(DetailView):
    template_name = 'rate/rate_details.html'
    queryset = Rate.objects.all()


class RateUpdateView(UpdateView):
    form_class = RateForm
    template_name = 'rate/rate_update.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class RateDeleteView(DeleteView):
    template_name = 'rate/rate_delete.html'
    queryset = Rate.objects.all()
    success_url = reverse_lazy('currency:rate-list')


class ContactUsCreateView(SendMessageMixin, CreateView):
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


class ContactUsUpdateView(SendMessageMixin, UpdateView):
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
