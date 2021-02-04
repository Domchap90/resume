from django.contrib import admin
from .models import Blog, Subscriber


class BlogAdmin(admin.ModelAdmin):

    list_display = ('blog_post_date', 'id', 'blog_title', 'blog_file')

    ordering = ('-blog_post_date', 'blog_title')


class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'number')

    ordering = ('name', 'email')


admin.site.register(Blog, BlogAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

