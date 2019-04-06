import os
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


# Available registries, order does matter
PALETTE_AVAILABLE_REGISTRIES = [
    # Legacy one, Based on CSS color name standard. Have a clean grey
    # names structure.
    ("Web names", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "colors/datas", "default.json")),

    # A very large palette (~4160) with great variety
    # Disabled because involves longer time
    # ("Dulux", os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                        "colors/datas", "dulux.json")),

    # Short (~120 names) but bring some new vocabulary, lacks of greys
    ("Crayola", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "colors/datas", "crayola.json")),

    # A big palette (~950)
    ("Xkcd", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "colors/datas", "xkcd.json")),
]
