from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Blog
from cms.forms import SubscriberForm
from cms.models import Subscriber
import os
import re

from tika import parser


def blog(request):
    blogs = Blog.objects.order_by('-post_date')
    blog_extract_list = []

    for blog in blogs:
        print(f"image = {blog.image}")
        file_path = os.path.join(settings.MEDIA_ROOT, str(blog.file))
        parsed_pdf = parser.from_file(file_path)
        pdf_content = parsed_pdf['content']

        pdf_extract = get_blog_extract(pdf_content, 250)
        blog_extract_list.append([blog, pdf_extract])

    pagenum = request.GET.get('pagenum', 1)

    blogs_paginated = Paginator(blog_extract_list, 5)

    try:
        blog_page_objects = blogs_paginated.page(pagenum)
    except PageNotAnInteger:
        blog_page_objects = blogs_paginated.page(1)
    except EmptyPage:
        blog_page_objects = blogs_paginated.page(blogs_paginated.num_pages)

    form = SubscriberForm()

    if request.POST:
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

            notify_subscriber_on_signup(subscriber)
            # reset empty form
            form = SubscriberForm()

    context = {
        'blogs': blog_page_objects,
        'sub_signup_form': form
    }

    return render(request, 'blog/blog.html', context)


def get_blog_extract(content, extract_len):
    # Get first 175 characters of each blog that aren't title

    content = content.strip()
    lines = re.split('\n', content)
    empty_line_counter = 0
    char_counter = 0
    extract = ""

    for line in lines:
        remaining_chars = extract_len - char_counter
        if empty_line_counter < 2 and re.match("^\\s*$", line):
            empty_line_counter += 1
        elif empty_line_counter == 2:
            if char_counter < extract_len:
                if len(line) <= remaining_chars:
                    char_counter += len(line)
                    extract += line
                else:
                    char_counter += remaining_chars
                    extract += line[:remaining_chars]

        if char_counter == extract_len:
            break

    return extract + "..."


def notify_subscriber_on_signup(recipient):
    subject = "Sign up DC mailing list"
    message = render_to_string('blog/email/body.txt', {'name': recipient.name})
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [recipient.email], fail_silently=False)
    except IOError:
        # Will catch both SMTPException AND socket.error
        print("Unable to send email at this time.")
