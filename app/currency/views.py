from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from currency.models import Rate, ContactUs
from currency.forms import RateForm, ContactUsForm


# main page
def index(request):
    context = {}
    return render(request, 'index.html', context)


def rate_create(request):
    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/rate/list")
    elif request.method == "GET":
        form = RateForm()
    context = {"form": form}
    return render(request, "rate_create.html", context)


def rate_list(request):
    result = Rate.objects.all()
    context = {'rate_list': result}
    return render(request, 'rate_list.html', context)


def rate_details(request, pk):
    rate_by_id = get_object_or_404(Rate, pk=pk)
    context = {'rate': rate_by_id}
    return render(request, 'rate_details.html', context)


def rate_update(request, pk):
    rate_by_id = get_object_or_404(Rate, pk=pk)
    if request.method == "POST":
        form = RateForm(request.POST, instance=rate_by_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/rate/list")
    elif request.method == "GET":
        form = RateForm(instance=rate_by_id)
    context = {"form": form}
    return render(request, "rate_update.html", context)


def rate_delete(request, pk):
    rate_by_id = get_object_or_404(Rate, pk=pk)
    if request.method == "POST":
        rate_by_id.delete()
        return HttpResponseRedirect("/rate/list")
    elif request.method == "GET":
        context = {"rate": rate_by_id}
        return render(request, "rate_delete.html", context)


def contact_us_create(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contact_us/list")
    elif request.method == "GET":
        form = ContactUsForm()
    context = {"form": form}
    return render(request, "contact_us_create.html", context)


def contact_us_list(request):
    result = ContactUs.objects.all()
    context = {'feedback_list': result}
    return render(request, 'contact_us_list.html', context)


def contact_us_details(request, pk):
    feedback_by_id = get_object_or_404(ContactUs, pk=pk)
    context = {'feedback': feedback_by_id}
    return render(request, 'contact_us_details.html', context)


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
    return render(request, "contact_us_update.html", context)


def contact_us_delete(request, pk):
    rate_by_id = get_object_or_404(ContactUs, pk=pk)
    if request.method == "POST":
        rate_by_id.delete()
        return HttpResponseRedirect("/contact_us/list")
    elif request.method == "GET":
        context = {"feedback": rate_by_id}
        return render(request, "contact_us_delete.html", context)
