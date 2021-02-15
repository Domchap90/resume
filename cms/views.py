from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from datetime import datetime

from .models import Blog, Subscriber
from .forms import BlogForm, SubscriberForm

import os


@staff_member_required
def cms(request):
    # Load blogs for CRUD operations
    blog_upload_form = BlogForm()
    add_subscriber_form = SubscriberForm()

    if request.POST.get('submit') == "upload_blog":
        blog_upload_form = add_blog(request)
    elif request.POST.get('submit') == "add_subscriber":
        add_subscriber_form = add_subscriber(request)

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

    subscribers = Subscriber.objects.order_by('name')
    edit_sub_forms = []

    for sub in subscribers:

        data = {
            'id': sub.id,
            'name': sub.name,
            'email': sub.email,
            'number': sub.number
        }

        edit_sub_forms.append(SubscriberForm(data))

    context = {
        'blogs': blogs,
        'blog_upload_form': blog_upload_form,
        'edit_blog_forms': edit_blog_forms,
        'subscribers': subscribers,
        'add_sub_form': add_subscriber_form,
        'edit_sub_forms': edit_sub_forms,
    }

    return render(request, 'cms/cms.html', context)


@staff_member_required
def add_blog(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
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


@staff_member_required
def edit_blog(request):
    id = request.POST.get('id')
    blog = Blog.objects.get(id=id)
    blog.blog_file = request.FILES.get('blog_file')

    blog.blog_title = request.POST.get('blog_title')
    blog.blog_post_date = get_form_date(request.POST.get('blog_post_date'))
    blog.save()

    return redirect('cms')


@staff_member_required
def delete_blog(request):
    title = request.POST.get('unique_property')
    Blog.objects.get(blog_title=title).delete()

    return HttpResponse(status=200)


@staff_member_required
def delete_subscriber(request):
    email = request.POST.get('unique_property')
    Subscriber.objects.get(email=email).delete()

    return HttpResponse(status=200)


@staff_member_required
def add_subscriber(request):
    form = SubscriberForm(request.POST)
    name = request.POST.get('name')
    email = request.POST.get('email')
    number = request.POST.get('number')

    if form.is_valid():
        subscriber = Subscriber(
            name=name,
            email=email,
            number=number)
        subscriber.save()

    return form


@staff_member_required
def edit_subscriber(request):
    sub_id = request.POST.get('id')
    subscriber = Subscriber.objects.get(id=sub_id)
    subscriber.name = request.POST.get('name')
    subscriber.email = request.POST.get('email')
    subscriber.number = request.POST.get('number')
    subscriber.save()

    return redirect('cms')


def get_form_date(entry):
    # if date field empty defaults to current date
    return datetime.now().date() if entry == '' else entry
