#!/usr/bin/env python
"""
A very basic script to build some deployment configurations from templates
and with project context.
"""
import os
from importlib import util

from jinja2 import Environment, FileSystemLoader, select_autoescape


class ConfigBuilder:
    """
    Import settings from Django to get the real context to give to configuration
    templates and build them.
    """
    def __init__(self, settings_path, template_dir="templates"):
        modpath = settings_path
        modname = os.path.splitext(os.path.basename(modpath))[0]
        self.settings = self.import_file(modname, modpath)

        template_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                template_dir,
            )
        )
        self.template_dir = template_dir

        self.jinja_env = self.get_jinjaenv()

    def import_file(self, full_name, path):
        """
        Import a python module from a path.

        Supported from Python>=3.5

        Arguments:
            full_name (string): Module name to import from path. If the path is a
                module, like "/home/foo.py" it should be "foo".
            path (string): Path to search for module.

        Returns:
            object: Imported module.
        """
        spec = util.spec_from_file_location(full_name, path)
        mod = util.module_from_spec(spec)

        spec.loader.exec_module(mod)
        return mod

    def get_jinjaenv(self):
        """
        Start Jinja environment.

        Returns:
            jinja2.Environment: Initialized Jinja environment.
        """
        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(["html", "xml"])
        )

        return env

    def get_template(self, filepath):
        """
        Load and return Jinja template.

        Arguments:
            filepath (string): Filepath to the template from its registered
                location in Jinja environment.

        Returns:
            jinja2.Template: Template ready to render.
        """

        return self.jinja_env.get_template(filepath)

    def get_context(self, extra={}):
        """
        Return context.

        Arguments:
            extra (dict): Extra context which items will override the initial one.

        Returns:
            dict: The context.
        """
        context = {
            "MEDIA_ROOT": os.path.normpath(self.settings.MEDIA_ROOT),
            "STATIC_ROOT": os.path.normpath(self.settings.STATIC_ROOT),
            "BASE_DIR": os.path.normpath(self.settings.BASE_DIR),
            "VAR_DIR": os.path.normpath(self.settings.VAR_DIR),
            "WSGI_APPLICATION": self.settings.WSGI_APPLICATION,
        }

        context.update(extra)

        return context

    def render(self, template_name, context={}):
        """
        Render document.

        Rendered document is serialized to JSON string inside ``content``
        item in document dict.

        Arguments:
            template_name (string): Path to template file relative to template_dir

        Returns:
            string: Rendered document.
        """
        document = self.get_template(template_name)

        return document.render(**self.get_context())

    def build(self, configs):
        """
        Should build config files from templates and context.

        Arguments:
            configs (list): List of tuples for templates names and destination for each
                config.
        """
        for template_name, destination in configs:
            print(
                self.render(template_name)
            )


if __name__ == "__main__":
    builder = ConfigBuilder(
        "/home/emencia/Projects/Apps/DjangoPalette-dev/sandbox/settings/demo.py"
    )

    import json
    print("CONTEXT")
    print("===============")
    print(
        json.dumps(builder.get_context(), indent=4)
    )
    print()

    builder.build([
        ("gunicorn_start", "../etc/gunicorn_start"),
    ])
