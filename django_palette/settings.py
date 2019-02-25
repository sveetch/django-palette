from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _


PALETTE_DUMP_FORMATS = OrderedDict([
    ("json", {
        "name": _("JSON"),
        "template": "django_palette/dumps/json.txt",
    }),
    ("python-dict", {
        "name": _("Python dictionnary"),
        "template": "django_palette/dumps/python_dict.txt",
    }),
    ("scss-vars", {
        "name": _("Scss variables"),
        "template": "django_palette/dumps/scss_variables.txt",
    }),
    ("html-snippet", {
        "name": _("HTML snippet"),
        "template": "django_palette/dumps/html_snippet.txt",
    }),
    ("sveetoy", {
        "name": _("Sveetoy color schemes"),
        "template": "django_palette/dumps/sveetoy.txt",
    }),
    ("php", {
        "name": _("PHP array"),
        "template": "django_palette/dumps/php.txt",
    }),
])
