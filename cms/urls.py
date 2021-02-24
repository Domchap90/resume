from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cms, name='cms'),
    path('delete_blog/<str:title>',
         views.delete_blog, name='deleteblog'),
    path('edit_blog/', views.edit_blog, name='edit_blog'),
    path('edit_subscriber/', views.edit_subscriber, name='edit_subscriber'),
    path('delete_subscriber/<str:email>', views.delete_subscriber,
         name='delete_subscriber'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
