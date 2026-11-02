"""
Eventix URL Configuration
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Eventix_project/wsgi.py', event_views.home_view, name='wsgi_fallback'),
    path('', include('events.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
