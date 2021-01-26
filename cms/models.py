from django.db import models


class Blog(models.Model):
    blog_file = models.FileField(
        upload_to='blogs/%Y/%m/%d')
    blog_title = models.CharField(max_length=50, unique=True)
    blog_post_date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_title
