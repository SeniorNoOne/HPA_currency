from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
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


def contact_us_create(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contact_us/list")
    elif request.method == "GET":
        form = ContactUsForm()
    context = {"form": form}
    return render(request, "contact_us/contact_us_create.html", context)


def contact_us_list(request):
    result = ContactUs.objects.all()
    context = {'feedback_list': result}
    return render(request, 'contact_us/contact_us_list.html', context)


def contact_us_details(request, pk):
    feedback_by_id = get_object_or_404(ContactUs, pk=pk)
    context = {'feedback': feedback_by_id}
    return render(request, 'contact_us/contact_us_details.html', context)


def contact_us_update(request, pk):
    rate_by_id = get_object_or_404(ContactUs, pk=pk)
    if request.method == "POST":
        form = ContactUsForm(request.POST, instance=rate_by_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contact_us/list")
    elif request.method == "GET":
        form = ContactUsForm(instance=rate_by_id)
    context = {"form": form}
    return render(request, "contact_us/contact_us_update.html", context)


def contact_us_delete(request, pk):
    rate_by_id = get_object_or_404(ContactUs, pk=pk)
    if request.method == "POST":
        rate_by_id.delete()
        return HttpResponseRedirect("/contact_us/list")
    elif request.method == "GET":
        context = {"feedback": rate_by_id}
        return render(request, "contact_us/contact_us_delete.html", context)


def source_create(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/source/list")
    elif request.method == "GET":
        form = SourceForm()
    context = {"form": form}
    return render(request, "source/source_create.html", context)


def source_list(request):
    result = Source.objects.all()
    context = {'source_list': result}
    return render(request, 'source/source_list.html', context)


def source_details(request, pk):
    source_by_id = get_object_or_404(Source, pk=pk)
    context = {'source': source_by_id}
    return render(request, "source/source_details.html", context)


def source_update(request, pk):
    source_by_id = get_object_or_404(Source, pk=pk)
    if request.method == "POST":
        form = SourceForm(request.POST, instance=source_by_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/source/list")
    elif request.method == "GET":
        form = SourceForm(instance=source_by_id)
    context = {"form": form}
    return render(request, "source/source_update.html", context)


def source_delete(request, pk):
    source_by_id = get_object_or_404(Source, pk=pk)
    if request.method == "POST":
        source_by_id.delete()
        return HttpResponseRedirect("/source/list")
    elif request.method == "GET":
        context = {"source": source_by_id}
        return render(request, "source/source_delete.html", context)
