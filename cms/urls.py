from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cms, name='cms'),
    path('blog_content', views.blog_content, name='blog_content'),
    path('delete_blog/', views.delete_blog, name='delete_blog')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
