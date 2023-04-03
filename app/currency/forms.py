from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms

from currency.models import Rate, ContactUs, Source


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'buy',
            'sell',
            'source',
            'currency'
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
            Row(Column('buy', css_class='col-6'),
                Column('sell', css_class='col-6'),
                css_class='row justify-content-center'),
            Row(Column('source', css_class='col-6'),
                Column('currency', css_class='col-6'),
                css_class='row justify-content-center'),
            Row(Column(Submit('submit', 'Submit', css_class='btn btn-primary col-2')))
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
            'message': forms.Textarea(attrs={'placeholder': 'Provide us your detailed feedback',
                                             'rows': '10'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('email_from', css_class='col-6'),
                Column('subject', css_class='col-6'),
                css_class='row justify-content-center'),
            Row(Column('message', args={'rows': '10'}),
                css_class='row justify-content-center'),
            Row(Column(Submit('submit', 'Submit', css_class='btn btn-primary col-2')))
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'source_url',
            'name',
            'city',
            'phone'
        )
        widgets = {
            'source_url': forms.TextInput(attrs={'placeholder': 'Enter source URL'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter source name'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter source city'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter source phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(Column('source_url', css_class='col-6'),
                Column('name', css_class='col-6'),
                css_class='row justify-content-center'),
            Row(Column('city', css_class='col-6'),
                Column('phone', css_class='col-6'),
                css_class='row justify-content-center'),
            Row(Column(Submit('submit', 'Submit', css_class='btn btn-primary col-2')))
        )
