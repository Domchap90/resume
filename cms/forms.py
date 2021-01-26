from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as ugtl

from .models import Blog


class BlogForm(forms.Form):
    blog_file = forms.FileField(
        label='Upload File',
        help_text='max. 42 megabytes',
        # validators=[
        #     FileTypeValidator(
        #         allowed_types=['text/plain'], allowed_extensions=['.txt'])
        #     ]
    )
    blog_title = forms.CharField(max_length=50)
    blog_post_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS, required=False)

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
