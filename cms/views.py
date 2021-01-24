from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from .models import Blog
from .forms import BlogForm


def cms(request):
    print("cms view accessed.")
    # Load blogs for CRUD operations
    print(f"blog submit val = {dict(request.POST.lists())}")
    if request.POST:
        print(f"request.POST = {request.POST}")
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
    print("blog content accessed.")
    form = BlogForm(request.POST, request.FILES)
    date_entered = request.POST.get('blog_post_date')

    # if date field empty defaults to current date
    date = datetime.now().date() if date_entered == '' else date_entered

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

    # blogs = Blog.objects.order_by('-blog_post_date')
    
    return form


# def email_subscribers(request):