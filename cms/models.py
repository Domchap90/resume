from django.db import models
from django.core.validators import validate_email
from phonenumber_field.modelfields import PhoneNumberField


class Blog(models.Model):
    blog_file = models.FileField(
        upload_to='blogs/%Y/%m/%d')
    blog_title = models.CharField(max_length=50, unique=True)
    blog_post_date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_title


class Subscriber(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, null=False, blank=False,
                              validators=[validate_email])
    number = PhoneNumberField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + ": " + self.email
