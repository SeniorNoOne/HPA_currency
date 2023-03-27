from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.views.generic import CreateView, RedirectView, UpdateView
from django.urls import reverse_lazy
from account.forms import UserSignUpForm
from utils.mixins import SendSignupMailMixin
from django.core.files.base import ContentFile


class UserSignupView(SendSignupMailMixin, CreateView):
    queryset = get_user_model().objects.all()
    template_name = "signup.html"
    success_url = reverse_lazy("index")
    form_class = UserSignUpForm


class UserActivateView(RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        username = kwargs.pop('username')

        user = get_user_model().objects.filter(username=username).only('id').first()
        if user is not None:
            user.is_active = True
            user.save(update_fields=['is_active'])

        url = super().get_redirect_url(*args, **kwargs)
        return url


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('index')
    queryset = get_user_model().objects.all()
    fields = (
        'first_name',
        'last_name',
        'avatar'
    )

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        instance = form.save(commit=False)

        uploaded_file = form.cleaned_data['avatar']

        if uploaded_file:
            filename = default_storage.save(instance.username + '/' + uploaded_file.name,
                                            ContentFile(uploaded_file.read()))
            instance.avatar = filename
        else:
            instance.avatar = None
        instance.save()
        return super().form_valid(form)
