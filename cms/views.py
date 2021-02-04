from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from datetime import datetime

from .models import Blog
from .forms import BlogForm

import os


def cms(request):
    # Load blogs for CRUD operations
    if request.POST:
        blog_upload_form = blog_content(request)
    else:
        blog_upload_form = BlogForm()

    blogs = Blog.objects.order_by('-blog_post_date')
    edit_blog_forms = []
    for blog in blogs:

        data = {
            'id': blog.id,
            'blog_title': blog.blog_title,
            'blog_post_date': blog.blog_post_date
        }

        file_content = os.path.join(
            settings.MEDIA_ROOT, blog.blog_file.name).encode()

        file_data = {'blog_file': SimpleUploadedFile(
            blog.blog_file.name, file_content)}

        edit_blog_forms.append(BlogForm(data, file_data))

    context = {
        'blogs': blogs,
        'upload_form': blog_upload_form,
        'edit_forms': edit_blog_forms
    }

    return render(request, 'cms/cms.html', context)


def blog_content(request):
    form = BlogForm(request.POST, request.FILES)
    date = get_form_date(request.POST.get('blog_post_date'))
    print(f"date = {date}")
    title = request.POST.get('blog_title')
    bfile = request.FILES.get('blog_file', None)

    if form.is_valid():
        print('form is valid.')
        blogpost = Blog(
            blog_file=bfile,
            blog_title=title,
            blog_post_date=date)
        blogpost.save()

    return form


def edit_blog(request):
    id = request.POST.get('id')
    print(f"EDIT_BLOG: id = {id}")
    blog = Blog.objects.get(id=id)
    blog.blog_file = request.FILES.get('blog_file')
    # file not showing up
    blog.blog_title = request.POST.get('blog_title')
    blog.blog_post_date = get_form_date(request.POST.get('blog_post_date'))
    blog.save()
    print(f"file = {blog.blog_file}, title = {blog.blog_title}, date = {blog.blog_post_date}")
    return redirect('cms')


def delete_blog(request):
    print("delete_blog entered")
    title = request.POST.get('blog_title')
    print(f"title = {title}")
    Blog.objects.get(blog_title=title).delete()

    return HttpResponse(status=200)
    # return HttpResponse('cms')


def get_form_date(entry):
    # if date field empty defaults to current date
    return datetime.now().date() if entry == '' else entry


# def email_subscribers(request):