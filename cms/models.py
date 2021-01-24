from django.db import models
from django.conf import settings


class Blog(models.Model):
    blog_file = models.FileField(
        upload_to='blogs/%Y/%m/%d',
        help_text="Formats accepted: txt only")
    blog_title = models.CharField(max_length=50)
    blog_post_date = models.DateField()

    def save(self, *args, **kwargs):
        print(f"Save accessed - blog title is {self.blog_title}, blog file is {self.blog_file}, blog date is {self.blog_post_date}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_title
