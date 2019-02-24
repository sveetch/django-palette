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

# This is only needed when using runserver with demo settings
if settings.DEBUG:
    urlpatterns = (
        urlpatterns
        + [
            path('styleguide/', include('sandbox.styleguide.urls')),
            path('prototypes/', include('sandbox.prototypes.urls')),
        ]
        + staticfiles_urlpatterns()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
