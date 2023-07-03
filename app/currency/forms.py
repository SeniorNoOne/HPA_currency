from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row, Submit

from currency.constants import RateFilterConfig
from currency.models import ContactUs, Rate, Source


class RateFilterForm(forms.Form):
    buy__lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.buy,
        required=False
    )
    buy = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter buy value'}),
        required=False
    )

    sell__lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.sell,
        required=False
    )
    sell = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Enter sell value'}),
        required=False
    )

    source__name__lookup = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=RateFilterConfig.source_name,
        required=False
    )
    source__name = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter source name'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('buy__lookup', css_class='col-6 mt-3'),
                Column('buy', css_class='col-6 align-self-end mt-3'),
            ),
            Row(
                Column('sell__lookup', css_class='col-6 mt-3'),
                Column('sell', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column('source__name__lookup', css_class='col-6 mt-3'),
                Column('source__name', css_class='col-6 mt-3 align-self-end')
            ),
            Row(
                Column(
                    Submit('submit', 'Apply', css_class='btn btn-primary col-12'),
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
