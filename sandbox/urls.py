"""
Sandbox URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.static import serve


urlpatterns = [
    path('', include('django_palette.urls')),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        urlpatterns
        + staticfiles_urlpatterns()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
