from django.db import models


class Blog(models.Model):
    file = models.FileField(
        upload_to='blogs/%Y/%m/%d')
    title = models.CharField(max_length=75, unique=True)
    post_date = models.DateField(blank=True, null=True)
    image = models.FileField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
