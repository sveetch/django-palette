# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormMixin

from django_palette.forms.source import SourceForm
from django_palette.views import JsonResponseBadRequest


class IndexView(TemplateView):
    """
    Just display the SourceForm but does not accept POST request.
    """
    template_name = 'django_palette/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SourceForm()
        return context


class SourceFormView(FormMixin, View):
    """
    Dedicated view to receive SourceForm POST request.
    """
    form_class = SourceForm
    http_method_names = ['post', 'head', 'options']

    def form_valid(self, form):
        """
        Return JSON from SourceForm.save
        """
        return JsonResponse({'data': form.save()})

    def form_invalid(self, form):
        """
        Return errors as JSON inside HEAD response with proper http error
        """
        return JsonResponseBadRequest({'data': form.errors})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
