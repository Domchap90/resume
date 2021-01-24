from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cms, name='cms'),
    path('blog_content', views.blog_content, name='blog_content'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
