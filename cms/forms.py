from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as ugtl
from upload_validator import FileTypeValidator


class BlogForm(forms.Form):
    blog_file = forms.FileField(
        label='Upload File',
        help_text='max. 42 megabytes',
        validators=[
            FileTypeValidator(
                allowed_types=['text/plain'], allowed_extensions=['.txt'])
            ]
    )
    blog_title = forms.CharField(max_length=50)
    blog_post_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS, required=False)

    def clean_blog_file(self):
        blog_file = self.cleaned_data['blog_file']
        # content_type = blog_file.content_type.split('/')[0]
        # if content_type in settings.CONTENT_TYPES:
        print(f"blog_file size = {blog_file.size}")
        if blog_file.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(
                ugtl(
                    'Please keep filesize under %s. Current filesize %s'
                    ) % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE),
                        filesizeformat(blog_file.size)
                        ))
        # else:
        #     raise forms.ValidationError(ugtl('blog_file type is not supported'))
        return blog_file
