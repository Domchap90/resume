from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):

    list_display = ('blog_post_date', 'id', 'blog_title', 'blog_file')

    ordering = ('-blog_post_date', 'blog_title')


admin.site.register(Blog, BlogAdmin)
