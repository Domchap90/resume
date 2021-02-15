from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as ugtl
from phonenumber_field.formfields import PhoneNumberField

from .models import Blog


class BlogForm(forms.Form):
    blog_file = forms.FileField(
        label='Upload File',
        help_text='max. 42 megabytes',
    )
    blog_title = forms.CharField(max_length=50)
    blog_post_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS, required=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_blog_file(self):
        blog_file = self.cleaned_data['blog_file']
        extension = ''
        if '.' in str(blog_file):
            extension = str(blog_file).split('.')[1]

        if extension == "txt":
            if blog_file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    ugtl(
                        'Please keep filesize under %s. Current filesize %s'
                        ) % (
                            filesizeformat(settings.MAX_UPLOAD_SIZE),
                            filesizeformat(blog_file.size)
                            ))
        else:
            raise forms.ValidationError(
                ugtl(
                    "This file extension cannot be accepted. \
Files must be '.txt'."))
        return blog_file

    def clean_blog_title(self):
        # Ensure title is unique
        blog_title = self.cleaned_data['blog_title']
        title_list = []
        for blog in Blog.objects.all():
            title_list.append(blog.blog_title)

        if blog_title in title_list:
            raise forms.ValidationError("This title already exists.")


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
    #     labels = {
    #         'name': 'Name',
    #         'email': 'Email Address',
    #         'number': 'Contact Number',
    #     }

       

    #     for field in self.fields:
    #         self.fields[field].label = labels[field]
    #         self.fields[field].widget.attrs['placeholder'] = f'{placeholders[field]}'
    #         if field != "number":
    #             self.fields[field].required = True
    #             self.fields[field].label += '*'
