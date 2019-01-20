import json

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


DUMP_FORMATS_CHOICES = [(k, v["name"]) for k,v in settings.PALETTE_DUMP_FORMATS.items()]


class DumpForm(forms.Form):
    """
    Form to build dumps from given palette and according to selected formats
    """
    palette = forms.CharField(
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
        palette = self.cleaned_data.get("palette")

        if palette:
            # Validate JSON syntax
            try:
                data = json.loads(palette)
            except json.decoder.JSONDecodeError:
                raise ValidationError(
                    _('Invalid JSON data.'),
                    code='invalid',
                )
            else:
                # Validate data is not empty
                if not data:
                    raise ValidationError(
                        _('This field is required.'),
                        code='invalid',
                    )
                else:
                    # validate data is a list
                    if not isinstance(data, list):
                        raise ValidationError(
                            _('Palette data structure is invalid.'),
                            code='invalid',
                        )

                    # Validate structure
                    # Although validation logs some explicit errors it is
                    # not returned to avoid too long message error, keep it
                    # simple.
                    structure_errors = self.validate_palette_structure(data)
                    if structure_errors:
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
        # TODO: From selected formats, build their dump from given palette

        print(self.cleaned_data["formats"])

        for format_name in self.cleaned_data["formats"]:
            format_opts = settings.PALETTE_DUMP_FORMATS[format_name]
            print(format_opts["template"])

        return "todo"
