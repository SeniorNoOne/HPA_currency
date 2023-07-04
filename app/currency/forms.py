from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row, Submit

from currency.constants import RateFilterConfig, ContactUsFilterConfig, SourceFilterConfig, \
    RequestResponseLogFilterConfig
from currency.models import ContactUs, Rate, Source
from currency.choices import RateCurrencyChoices, RequestMethodChoices


# Create and Update forms
class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'buy',
            'sell',
            'source',
            'currency',
        )
        widgets = {
            'buy': forms.NumberInput(attrs={'placeholder': 'Enter buying rate'}),
            'sell': forms.NumberInput(attrs={'placeholder': 'Enter selling rate'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('buy', css_class='col-4'),
                Column('sell', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('source', css_class='col-4'),
                Column('currency', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary col-2'),
                    css_class='offset-2'
                )
            )
        )


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'subject',
            'message',
        )
        widgets = {
            'email_from': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject'}),
            'message': forms.Textarea(
                attrs={
                    'placeholder': 'Provide us your detailed feedback',
                    'rows': '10',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('email_from', css_class='col-4'),
                Column('subject', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('message', args={'rows': '10'}, css_class='col-8 '),
                css_class='row justify-content-center'
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary col-2'),
                    css_class='offset-2'
                )
            )
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'logo',
            'url',
            'name',
            'code',
            'city',
            'phone'
        )
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'Enter source URL'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter source name'}),
            'code': forms.NumberInput(attrs={'placeholder': 'Enter unique source code'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter source city'}),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter source phone number',
                    'data-mask': '+000-00-000-00-00',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('logo', css_class='col-8'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('url', css_class='col-8'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('name', css_class='col-4'),
                Column('code', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column('city', css_class='col-4'),
                Column('phone', css_class='col-4'),
                css_class='row justify-content-center'
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary col-2'),
                    css_class='offset-2'
                )
            )
        )


# Filter forms
class RateFilterForm(forms.Form):
    buy_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.buy,
        required=False
    )
    buy = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Enter buy value'}),
        required=False
    )

    sell_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.sell,
        required=False
    )
    sell = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Enter sell value'}),
        required=False
    )

    source_name_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.source__name,
        required=False
    )
    source_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter source name'}),
        required=False
    )

    currency_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.currency,
        required=False
    )
    currency = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateCurrencyChoices.choices,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('buy_lookup', css_class='col-6 mt-3'),
                Column('buy', css_class='col-6 mt-3 align-self-end'),
            ),
            Row(
                Column('sell_lookup', css_class='col-6 mt-3'),
                Column('sell', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column('source_name_lookup', css_class='col-6 mt-3'),
                Column('source_name', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column('currency_lookup', css_class='d-none'),
                Column('currency', css_class='col-12 mt-3'),
            ),
            Row(
                Column(
                    Submit('', 'Apply', css_class='btn btn-primary col-12'),
                    css_class='col-6'
                ),
                Column(
                    HTML(
                        '<a href="{% url "currency:rate-list" %}"'
                        'class="btn btn-danger col-12" role="button">Reset</a>'
                    ),
                    css_class='col-6'
                )
            )
        )


class ContactUsFilterForm(forms.Form):
    email_from_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ContactUsFilterConfig.email_from,
        required=False
    )
    email_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter email'}),
        required=False
    )

    subject_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ContactUsFilterConfig.subject,
        required=False
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter subject'}),
        required=False
    )

    message_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=ContactUsFilterConfig.message,
        required=False
    )
    message = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter message'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('email_from_lookup', css_class='col-6 mt-3'),
                Column('email_from', css_class='col-6 mt-3 align-self-end'),
            ),
            Row(
                Column('subject_lookup', css_class='col-6 mt-3'),
                Column('subject', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column('message_lookup', css_class='col-6 mt-3'),
                Column('message', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column(
                    Submit('', 'Apply', css_class='btn btn-primary col-12'),
                    css_class='col-6'
                ),
                Column(
                    HTML(
                        '<a href="{% url "currency:contactus-list" %}"'
                        'class="btn btn-danger col-12" role="button">Reset</a>'
                    ),
                    css_class='col-6'
                )
            )
        )


class SourceFilterForm(forms.Form):
    url_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=SourceFilterConfig.url,
        required=False
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter url'}),
        required=False
    )

    name_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=SourceFilterConfig.name,
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter name'}),
        required=False
    )

    city_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=SourceFilterConfig.city,
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter city'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('url_lookup', css_class='col-6 mt-3'),
                Column('url', css_class='col-6 mt-3 align-self-end'),
            ),
            Row(
                Column('name_lookup', css_class='col-6 mt-3'),
                Column('name', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column('city_lookup', css_class='col-6 mt-3'),
                Column('city', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column(
                    Submit('', 'Apply', css_class='btn btn-primary col-12'),
                    css_class='col-6'
                ),
                Column(
                    HTML(
                        '<a href="{% url "currency:source-list" %}"'
                        'class="btn btn-danger col-12" role="button">Reset</a>'
                    ),
                    css_class='col-6'
                )
            )
        )


class RequestResponseLogFilterForm(forms.Form):
    path_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RequestResponseLogFilterConfig.path,
        required=False
    )
    path = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter path'}),
        required=False
    )

    request_method_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RequestResponseLogFilterConfig.request_method,
        required=False
    )
    request_method = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RequestMethodChoices.choices,
        required=False
    )

    time_lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RequestResponseLogFilterConfig.time,
        required=False
    )
    time = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Enter time value'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('path_lookup', css_class='col-6 mt-3'),
                Column('path', css_class='col-6 mt-3 align-self-end'),
            ),
            Row(
                Column('request_method_lookup', css_class='d-none'),
                Column('request_method', css_class='col-12 mt-3')
            ),
            Row(
                Column('time_lookup', css_class='col-6 mt-3'),
                Column('time', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column(
                    Submit('', 'Apply', css_class='btn btn-primary col-12'),
                    css_class='col-6'
                ),
                Column(
                    HTML(
                        '<a href="{% url "currency:log-list" %}"'
                        'class="btn btn-danger col-12" role="button">Reset</a>'
                    ),
                    css_class='col-6'
                )
            )
        )
