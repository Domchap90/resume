from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

from blog.models import Blog
from blog.forms import BlogForm
from .models import Subscriber
from .forms import SubscriberForm


@staff_member_required
def cms(request):
    # Load blogs for CRUD operations
    is_blog = None
    edit_id = None
    blog_upload_form = BlogForm()
    add_subscriber_form = SubscriberForm()

    if request.POST.get('submit') == "upload_blog":
        blog_upload_form = add_blog(request)
    elif request.POST.get('submit') == "add_subscriber":
        add_subscriber_form = add_subscriber(request)
    elif request.POST.get('submit') == "update_blog":
        is_blog = True
        edit_blog_form = edit_blog(request)
        edit_id = request.POST.get('id')
    elif request.POST.get('submit') == "update_subscriber":
        is_blog = False
        edit_sub_form = edit_subscriber(request)
        edit_id = request.POST.get('id')

    blogs = Blog.objects.all().order_by('-post_date')
    edit_blog_forms = {}

    for blog in blogs:
        if is_blog and edit_id == str(blog.id):
            # If edit ID is given for blogs attach blog edit form to dictionary
            edit_blog_forms[blog.id] = edit_blog_form
        else:
            b = Blog.objects.get(id=blog.id)
            edit_blog_forms[blog.id] = BlogForm(instance=b)

    subscribers = Subscriber.objects.order_by('name')
    edit_sub_forms = {}

    for sub in subscribers:
        if not is_blog and edit_id == str(sub.id):
            edit_sub_forms[sub.id] = edit_sub_form
        else:
            data = {
                'id': sub.id,
                'name': sub.name,
                'email': sub.email,
                'number': sub.number
            }
            edit_sub_forms[sub.id] = SubscriberForm(data)

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
    form = BlogForm(request.POST, request.FILES)
    date = get_form_date(request.POST.get('post_date'))
    title = request.POST.get('title')
    bfile = request.FILES.get('file', None)
    img = request.FILES.get('image')

    if form.is_valid():
        blogpost = Blog(
            file=bfile,
            title=title,
            post_date=date,
            image=img)
        blogpost.save()

    return form


@staff_member_required
def edit_blog(request):
    blog = Blog.objects.get(id=request.POST.get('id'))
    form = BlogForm(request.POST, request.FILES, instance=blog)

    if form.is_valid():
        form.save()

    return form


@staff_member_required
def delete_blog(request, title):
    Blog.objects.get(title=title).delete()

    return redirect('cms')


@staff_member_required
def delete_subscriber(request, email):
    Subscriber.objects.get(email=email).delete()

    return redirect('cms')


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
    data = {
        'id': request.POST.get('id'),
        'name': request.POST.get('name'),
        'email': request.POST.get('email'),
        'number': request.POST.get('number')
    }
    form = SubscriberForm(data)

    if form.is_valid():
        form.save()

    return form


def get_form_date(entry):
    # if date field empty defaults to current date
    return datetime.now().date() if entry == '' else entry
