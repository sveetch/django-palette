# -*- coding: utf-8 -*-
from django.conf.urls import url

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^frontend/$', TemplateView.as_view(
        template_name="prototypes/frontend_app.html")
    ),
]
