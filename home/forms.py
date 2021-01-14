from django import forms
from django.core.validators import validate_email


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Name', max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Smith'}))
    phone = forms.CharField(
        label='Contact Number', min_length=10, max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '01632 960481'}))
    email = forms.EmailField(
        label='Email', validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'username@domain.co.uk'}))
    message = forms.CharField(
        label='Message', max_length=500,
        widget=forms.Textarea(attrs={'placeholder': 'Tell me how i can help you...'})
                            )
