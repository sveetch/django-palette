import io
import os

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles import finders

from py_css_styleguide.model import Manifest


class StyleguideIndexView(TemplateView):
    """
    Display styleguide from CSS manifest
    """
    template_name = 'styleguide/index.html'

    def get_manifest(self, path):
        resolved_path = finders.find(path)

        manifest = Manifest()
        manifest.resolve_error = None

        if resolved_path:
            manifest_filepath = resolved_path

            with io.open(manifest_filepath, 'r') as fp:
                manifest.load(fp)
        else:
            msg = ("Unabled to find CSS manifest file from "
                   "statics: <code>{}</code>").format(path)
            manifest.resolve_error = msg


        return manifest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'styleguide': self.get_manifest(settings.STYLEGUIDE_MANIFEST_PATH),
        })

        return context
