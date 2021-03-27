from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as ugtl

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['file', 'title', 'post_date', 'image']

    def clean_file(self):
        file = self.cleaned_data['file']
        return validate_file_upload(
            file, ['pdf'], settings.MAX_FILE_UPLOAD_SIZE)

    def clean_image(self):
        image = self.cleaned_data['image']
        return validate_file_upload(
            image, ['png', 'jpg', 'jpeg', 'svg'], settings.MAX_IMG_UPLOAD_SIZE)

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'post_date':
                self.fields[field].required = True
                self.fields[field].label += '*'
            else:
                self.fields[field].required = False


def validate_file_upload(file_to_upload, accepted_extensions, max_size):
    """ Ensures file is of correct size and MIME type """

    extension = ''
    if '.' in str(file_to_upload):
        extension = str(file_to_upload).split('.')[1]

    if extension in accepted_extensions:
        if file_to_upload.size > max_size:
            raise forms.ValidationError(
                ugtl(
                    'Please keep filesize under %s. Current filesize %s'
                    ) % (
                        filesizeformat(max_size),
                        filesizeformat(file_to_upload.size)
                        ))
    else:
        raise forms.ValidationError(
            ugtl(
                "This file extension cannot be accepted. \
Files must be " + multiple_extensions_to_string(accepted_extensions) + "."))
    return file_to_upload


def multiple_extensions_to_string(extensions):
    """ Converts array of multiple file extensions to a string to be inserted in
        ValidationError raised by file cleaning methods. """

    length = len(extensions)
    multiple_string = 'either '
    if length > 1:
        for i, ext in enumerate(extensions):
            if (i < (length - 2)):
                multiple_string += "'" + ext + "', "
            elif (i == (length - 2)):
                multiple_string += "'" + ext + "' or "
            else:
                multiple_string += "'" + ext + "'"
    else:
        return "'" + extensions[0] + "'"

    return multiple_string
