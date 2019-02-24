"""
Django settings for demonstration

Intended to be used with ``make run``.
"""
from sandbox.settings.base import *

INSTALLED_APPS = INSTALLED_APPS + (
    'sandbox.styleguide',
    'sandbox.prototypes',
)

from django_palette.settings import *
