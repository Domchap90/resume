import hashlib
import json
import os
import re

import fitz
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

from cms.forms import SubscriberForm
from cms.models import Subscriber

from .models import Blog


def blog(request):
    blogs = Blog.objects.order_by('-post_date')
    blog_extract_list = []

    for blog in blogs:
        file_path = os.path.join(settings.MEDIA_ROOT, str(blog.file))
        file = fitz.open(file_path)
        blog_text = ""
        for page in file.pages(stop=1):
            blog_text += page.getText()

        pdf_extract = get_blog_extract(blog_text, 250)
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

            notify_subscriber_on_signup(request, subscriber)
            add_subscriber_to_mailchimp(request, subscriber)
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


def notify_subscriber_on_signup(request, recipient):
    """
    Emails user that they have succesfully signed up to the mailing list
    """

    subject = "Sign up DC mailing list"
    message = render_to_string('blog/email/body.txt', {'name': recipient.name})
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [recipient.email], fail_silently=False)
        messages.success(request, "Thank you for signing up. An email has been \
sent to {}, please check your inbox.".format(recipient.email))
    except IOError:
        # Will catch both SMTPException AND socket.error
        messages.error(request, "Unable to send email at this time. Please check the\
email address is valid and try again.")


def add_subscriber_to_mailchimp(request, user):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    # Mailchimp Settings
    api_key = settings.MAILCHIMP_API_KEY
    server = settings.MAILCHIMP_DATA_CENTER
    list_id = settings.MAILCHIMP_SUBSCRIBE_LIST_ID

    name_list = user.name.split(" ")
    fname = name_list[0]
    lname = ''
    if len(name_list) > 1:
        lname = name_list[1]

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": user.email,
        "status": "subscribed",
        'merge_fields': {
            'FNAME': fname,
            'LNAME': lname,
            'PHONE': str(user.number)
            }
    }

    try:
        mailchimp.lists.add_list_member(list_id, member_info)
    except ApiClientError as error:
        err_dict = json.loads(error.text)
        messages.error(request, "Unable to add to Mailchimp: {}".format(
            err_dict['detail']))


def delete_subscriber_from_mailchimp(request, member_email):
    """
     Deletes member selected from mailchimp
    """

    # Mailchimp Settings
    api_key = settings.MAILCHIMP_API_KEY
    server = settings.MAILCHIMP_DATA_CENTER
    list_id = settings.MAILCHIMP_SUBSCRIBE_LIST_ID

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_email_hash = hashlib.md5(
        member_email.encode('utf-8').lower()).hexdigest()
    member_update = {"status": "unsubscribed"}

    try:
        response = mailchimp.lists.update_list_member(
            list_id, member_email_hash, member_update)
        messages.success(
            request, "Member successfully unsubscribed. {}".format(response))
    except ApiClientError as error:
        err_dict = json.loads(error.text)
        messages.error(request, "Unable to delete from Mailchimp: {}".format(
            err_dict['detail']))


def read_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    file_path = str(blog.file)
    other_blogs = Blog.objects.all().order_by('-post_date').exclude(
        id=blog_id)[:3]

    context = {
        'blog': blog,
        'blog_file': file_path,
        'others': other_blogs
    }

    return render(request, 'blog/read_blog.html', context)


def pdf_view(request, year, month, day, filename):
    file_path = settings.MEDIA_ROOT + "/blogs/\
" + year + "/" + month + "/" + day + "/" + filename
    try:
        return FileResponse(
            open(file_path, 'rb'), content_type='application/pdf'
            )
    except FileNotFoundError:
        raise Http404
