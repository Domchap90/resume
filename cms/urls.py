from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cms, name='cms'),
    path('blog_content', views.blog_content, name='blog_content'),
    path('delete_blog/', views.delete_blog, name='delete_blog'),
    path('edit_blog/', views.edit_blog, name='edit_blog'),
    path('edit_subscriber/', views.edit_subscriber, name='edit_subscriber'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
