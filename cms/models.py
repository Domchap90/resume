from django.db import models
from django.core.validators import validate_email
from phonenumber_field.modelfields import PhoneNumberField


class Subscriber(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=80, null=False, blank=False,
                              validators=[validate_email])
    number = PhoneNumberField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Subscriber, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + ": " + self.email
