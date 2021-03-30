from django.contrib import admin

from .models import Blog


class BlogAdmin(admin.ModelAdmin):

    list_display = ('post_date', 'id', 'title', 'file', 'image')

    ordering = ('-post_date', 'title')


admin.site.register(Blog, BlogAdmin)
