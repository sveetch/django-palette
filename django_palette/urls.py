from django.urls import path

from django_palette.views.source import IndexView, SourceFormView
from django_palette.views.palette import PaletteFormView


app_name = 'django_palette'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('source/', SourceFormView.as_view(), name='source-post'),
    path('palette/', PaletteFormView.as_view(), name='palette-post'),
]
