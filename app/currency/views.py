from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from currency.forms import RateForm, ContactUsForm, SourceForm
from currency.models import Rate, ContactUs, Source


# main page
def index(request):
    context = {}
    return render(request, 'index.html', context)


class RateCreateView(CreateView):
    form_class = RateForm
    template_name = "rate/rate_create.html"
    queryset = Rate.objects.all()
    success_url = "/rate/list/"


class RateListView(ListView):
    template_name = "rate/rate_list.html"
    queryset = Rate.objects.all()


class RateDetailView(DetailView):
    template_name = "rate/rate_details.html"
    queryset = Rate.objects.all()


class RateUpdateView(UpdateView):
    form_class = RateForm
    template_name = "rate/rate_update.html"
    queryset = Rate.objects.all()
    success_url = "/rate/list/"


class RateDeleteView(DeleteView):
    template_name = "rate/rate_delete.html"
    queryset = Rate.objects.all()
    success_url = "/rate/list/"


class ContactUsCreateView(CreateView):
    form_class = ContactUsForm
    template_name = "contact_us/contact_us_create.html"
    queryset = ContactUs.objects.all()
    success_url = "/contact_us/list/"


class ContactUsListView(ListView):
    template_name = "contact_us/contact_us_list.html"
    queryset = ContactUs.objects.all()


class ContactUsDetailView(DetailView):
    template_name = "contact_us/contact_us_details.html"
    queryset = ContactUs.objects.all()


class ContactUsUpdateView(UpdateView):
    form_class = ContactUsForm
    template_name = "contact_us/contact_us_update.html"
    queryset = ContactUs.objects.all()
    success_url = "/contact_us/list/"


class ContactUsDeleteView(DeleteView):
    template_name = "contact_us/contact_us_delete.html"
    queryset = ContactUs.objects.all()
    success_url = "/contact_us/list/"


class SourceCreateView(CreateView):
    form_class = SourceForm
    template_name = "source/source_create.html"
    queryset = Source.objects.all()
    success_url = "/source/list/"


class SourceListView(ListView):
    template_name = "source/source_list.html"
    queryset = Source.objects.all()


class SourceDetailView(DetailView):
    template_name = "source/source_details.html"
    queryset = Source.objects.all()


class SourceUpdateView(UpdateView):
    form_class = SourceForm
    template_name = "source/source_update.html"
    queryset = Source.objects.all()
    success_url = "/source/list/"


class SourceDeleteView(DeleteView):
    template_name = "source/source_delete.html"
    queryset = Source.objects.all()
    success_url = "/source/list/"
