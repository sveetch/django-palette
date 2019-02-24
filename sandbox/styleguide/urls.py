# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url

from sandbox.styleguide.views import StyleguideIndexView

urlpatterns = [
    url(r'^$', StyleguideIndexView.as_view(), name='index'),
]
