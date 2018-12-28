from django.urls import path

from django_palette.views.source import IndexView, SourceFormView
from django_palette.views.palette import PaletteFormView
from django.views.decorators.csrf import ensure_csrf_cookie


app_name = 'django_palette'


urlpatterns = [
    path('', ensure_csrf_cookie(IndexView.as_view()), name='index'),
    path('source/', ensure_csrf_cookie(SourceFormView.as_view()), name='source-post'),
    path('palette/', ensure_csrf_cookie(PaletteFormView.as_view()), name='palette-post'),
]
