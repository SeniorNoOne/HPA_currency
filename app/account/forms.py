import uuid

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.password_validation import validate_password

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
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='col-8'),
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
        user.username = uuid.uuid4()
        user.set_password(password)
        user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mail'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )


class CustomResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your mail'})
    )
