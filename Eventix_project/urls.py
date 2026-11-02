"""
Eventix URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Eventix_project/wsgi.py', event_views.home_view, name='wsgi_fallback'),
    path('', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
