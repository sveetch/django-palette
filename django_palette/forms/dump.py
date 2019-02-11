import json

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..choices import DUMP_FORMATS_CHOICES
from ..dumps import build_dump


class DumpForm(forms.Form):
    """
    Form to build dumps from given palette and according to selected formats

    ``palette`` field is just a basic ``forms.Field`` since it just a JSON
    payload passed as is and we don't want it to be "stringified" (which lead
    to invalid single quoted JSON).
    """
    palette = forms.Field(
        label=_("Palette data"),
        required=True,
    )
    formats = forms.MultipleChoiceField(
        label=_("Formats"),
        required=True,
        choices=DUMP_FORMATS_CHOICES,
    )

    def clean_palette(self):
        """
        Validate named color is a name
        """
        palette = self.cleaned_data.get("palette", None)

        # Validate data is not empty
        if not palette:
            raise ValidationError(
                _('This field is required.'),
                code='invalid',
            )
        else:
            # validate data must be a list
            if not isinstance(palette, list):
                raise ValidationError(
                    _('Palette data structure is invalid.'),
                    code='invalid',
                )

            # Validate structure
            # Although validation logs some explicit errors it is
            # not returned to avoid too long message error, keep it
            # simple.
            errors = self.validate_palette_structure(palette)
            if errors:
                raise ValidationError(
                    _('Palette data structure is invalid.'),
                    code='invalid',
                )

        return palette

    def validate_palette_structure(self, data):
        """
        Validate given palette got valid expected structure to dump.
        """
        errors = []

        for i, item in enumerate(data):
            if "color" not in item:
                errors.append("Item #{} has no 'color' field".format(i))
            if "name" not in item:
                errors.append("Item #{} has no 'name' field".format(i))

        return errors

    def save(self, *args, **kwargs):
        dumps = []

        # Output dump formats respecting PALETTE_DUMP_FORMATS order
        for key, opts in settings.PALETTE_DUMP_FORMATS.items():
            if key in self.cleaned_data["formats"]:
                dumps.append(build_dump(key, self.cleaned_data.get("palette")))

        return dumps
