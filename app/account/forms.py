import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row, Submit

User = get_user_model()


class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = (
            'avatar',
            'email',
            'phone',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number',
                                            'data-mask': '+000-00-000-00-00'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML('<h3 class="text-center">Signup</h3>'),
                    css_class='col-8 mt-3'
                ),
                css_class='row justify-content-center'
            ),
            Row(
                Column('avatar', css_class='col-8'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('email', css_class='col-4'),
                Column('phone', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('first_name', css_class='col-4'),
                Column('last_name', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('password1', css_class='col-4'),
                Column('password2', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column(Submit('submit', 'Submit', css_class='btn btn-primary col-2'),
                       css_class='offset-2')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords should match!')
        validate_password(cleaned_data['password1'])
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.is_active = False
        user.username = user.username if user.username else uuid.uuid4()
        user.set_password(password)
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mail'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML('<h3 class="text-center">Login To Your Account</h3>'),
                    css_class='col-4 mt-3'
                ),
                css_class='row justify-content-center'
            ),
            Row(
                Column('username', css_class='col-4 mt-3'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('password', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column(Submit('submit', 'Login', css_class='btn btn-primary col-12'),
                       css_class='col-2'),
                Column(
                    HTML(
                        '<a href="{% url "password_reset" %}" '
                        'class="btn btn-danger col-12" role="button">Reset Password</a>'
                    ),
                    css_class='col-2'
                ),
                css_class='row justify-content-center',
            )
        )
