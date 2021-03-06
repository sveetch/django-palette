# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from django_palette.forms.dump import DumpForm
from django_palette.views import JsonResponseBadRequest, JsonFormPost


class DumpFormView(JsonFormPost, FormMixin, View):
    """
    Dedicated view to receive DumpForm POST request.
    """
    form_class = DumpForm
    http_method_names = ["post", "head", "options"]

    def form_valid(self, form):
        """
        Return JSON from DumpForm.save()
        """
        return JsonResponse({"data": form.save()})

    def form_invalid(self, form):
        """
        Return errors as JSON inside HEAD response with proper http error
        """
        return JsonResponseBadRequest({"data": form.errors})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it"s valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
