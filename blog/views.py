from django.conf import settings
from django.shortcuts import render
from .models import Blog
from tika import parser

import os
import re


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

    context = {
        'blogs': blog_extract_list,
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
