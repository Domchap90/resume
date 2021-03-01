from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Subscriber


class SubscriberForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=50, label='Name')
    email = forms.EmailField(
        max_length=80, label='Email Address')
    number = PhoneNumberField(label='Contact Number', required=False)

    def clean_number(self):
        number = self.cleaned_data['number']
        for sub in Subscriber.objects.all():
            if number == sub.number:
                raise forms.ValidationError(
                    "This number already exists within our records.")

        return number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'id': '',
            'name': "John Smith",
            'number': "+44 1632 960963 (Optional)",
            'email': "example@domain.co.uk",
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'placeholder': placeholders[field]})
