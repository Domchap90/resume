from . import views
from django.urls import path

urlpatterns = [
    path('', views.blog, name='blog'),
    path('read/<str:blog_id>', views.read_blog, name='read_blog'),
    path('read/pdf_view/blogs/<str:year>/<str:month>/<str:day>/<str:filename>',
         views.pdf_view, name='pdf_view')
]
