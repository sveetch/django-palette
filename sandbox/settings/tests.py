"""
Django settings for tests
"""
from sandbox.settings.base import *

# Avoid test fails from whitenoise on some app static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
