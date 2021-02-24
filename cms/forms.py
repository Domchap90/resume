from django import forms
from phonenumber_field.formfields import PhoneNumberField


class SubscriberForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=50, label='Name')
    email = forms.EmailField(
        max_length=80, label='Email Address')
    number = PhoneNumberField(label='Contact Number', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'id': '',
            'name': "User's name",
            'number': "If user wishes to be called (Optional)",
            'email': "Allows user to be emailed",
        }

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'placeholder': placeholders[field]})
