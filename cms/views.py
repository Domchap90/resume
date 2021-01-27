from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime

from .models import Blog
from .forms import BlogForm


def cms(request):
    # Load blogs for CRUD operations

    if request.POST:
        blog_form = blog_content(request)
    else:
        blog_form = BlogForm()

    blogs = Blog.objects.order_by('-blog_post_date')
    context = {
        'blogs': blogs,
        'form': blog_form
    }

    return render(request, 'cms/cms.html', context)


def blog_content(request):
    form = BlogForm(request.POST, request.FILES)
    date_entered = request.POST.get('blog_post_date')

    # if date field empty defaults to current date
    date = datetime.now().date() if date_entered == '' else date_entered
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
    title = request.POST.get('blog_title') 
    date =  get_form_date(request.POST.get('blog_date'))
    file = request.FILES.get('blog_file')

    return redirect('cms')


def delete_blog(request):
    print("delete_blog entered")
    title = request.POST.get('blog_title')
    print(f"title = {title}")
    Blog.objects.get(blog_title=title).delete()

    return HttpResponse(status=200)
    # return HttpResponse('cms')


def get_form_date(entry):
    return datetime.now().date() if entry == '' else entry


# def email_subscribers(request):