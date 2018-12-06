# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.forms import formset_factory
from django.views.generic.base import View
from django.views.generic.edit import FormMixin

from django_palette.forms.palette import (PaletteItemFormSet,
                                          PaletteItemForm)
from django_palette.views import JsonResponseBadRequest


class PaletteFormView(FormMixin, View):
    """
    Dedicated view to receive palette formset POST request.
    """
    http_method_names = ['post', 'head', 'options']
    form_class = formset_factory(
        PaletteItemForm,
        extra=0,
        formset=PaletteItemFormSet,
    )

    def form_valid(self, form):
        """
        Return JSON from PaletteItemFormSet.save
        """
        return JsonResponse({'data': form.save()})

    def form_invalid(self, form, nonform_errors=None):
        """
        Return errors as JSON inside HEAD response with proper http error.

        Non form errors are given through 'global' item.
        """
        errors = form.errors

        nonform_errors = nonform_errors or form.non_form_errors()
        if nonform_errors:
            errors.append({
                'global': nonform_errors
            })

        return JsonResponseBadRequest({
            'data': errors
        })

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()

        try:
            is_valid = form.is_valid()
        except ValidationError:
            return self.form_invalid(
                form,
                nonform_errors=["Malformed formset POST request"]
            )
        else:
            if is_valid:
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
