import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_palette.colors.naming import validate_name

from ..choices import DUMP_FORMATS_CHOICES

HEXADECIMAL_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")


def formset_data_helper(source_data, fields=True, initials=False):
    """
    From given SourceForm data return base data dict for formset with
    additional hidden field which contains dynamic choices as JSON string
    (required for each color name choices).

    Arguments:
        source_data (dict): Dictionnary of data.

    Keyword Arguments:
        fields (boolean): Add formset fields if enabled. Field items are
            ordered from ``sorted``.
        intials (boolean): Add initial values for each fields. Name value is
            allways color name from the first choice item. Enable this option
            without enabling ``fields`` option has no sense.

    Returns:
        dict: Data to give to formset initial argument.

    Sample source_data: ::

        {
            "#f0f0f0": [("gray94", "#f0f0f0")],
            "#ff0000": [("red1", "#ff0000"), ("firered", "#ff0000")],
            "#000000": [("black", "#000000")]
        }

    Sample output: ::

        {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "3",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#f0f0f0",
            "form-0-name": "gray94",
            "form-1-color": "#ff0000",
            "form-1-name": "red1",
            "form-2-color": "#000000",
            "form-2-name": "black",
            ...
        }

    Note how this helper only matter about first name choices from source_data.
    """
    output = {
        "form-TOTAL_FORMS": len(source_data),
        "form-INITIAL_FORMS": len(source_data),
        "form-MAX_NUM_FORMS": "",
    }

    if fields:
        for i, key in enumerate(sorted(source_data.keys())):
            value = source_data[key]
            if initials:
                output.update({
                    "form-{}-color".format(i): key,
                    "form-{}-name".format(i): value[0][0],
                })
            else:
                output.update({
                    "form-{}-color".format(i): "",
                    "form-{}-name".format(i): "",
                })

    return output


class PaletteItemFormSet(forms.BaseFormSet):
    """
    Formset to perform save on every form
    """
    def save(self, *args, **kwargs):
        return {
            "formats": DUMP_FORMATS_CHOICES,
            "palette": [f.save() for f in self.forms],
        }


class PaletteItemForm(forms.Form):
    """
    Form for palette item for Palette formset, each item is a color to name
    """
    color = forms.CharField(
        label=_("Color"),
        required=True,
    )
    name = forms.CharField(
        label=_("Name"),
        required=True,
        min_length=3,
        max_length=50,
    )

    def clean_color(self):
        """
        Validate color code is a valid hexadecimal (not rgb since its not
        supported).
        """
        code = self.cleaned_data.get("color")

        if code:
            # Allways lowercase color
            code = code.lower()

            if code.startswith("rgb"):
                raise ValidationError(
                    _("RGB(A) values are not supported"),
                    code="invalid",
                )
            elif code.startswith("#"):
                if not HEXADECIMAL_REGEX.search(code):
                    raise ValidationError(
                        _("Invalid Hexadecimal code"),
                        code="invalid",
                    )
            elif not code.isalpha():
                raise ValidationError(
                    _("Color name must only contain alphabetic characters"),
                    code="invalid",
                )

        return code

    def clean_name(self):
        """
        Validate named color is a name
        """
        name = self.cleaned_data.get("name")

        if name:
            # Allways lowercase name
            name = name.lower()

            if not validate_name(name):
                raise ValidationError(
                    _("Invalid name"),
                    code="invalid",
                )

        return name

    def save(self, *args, **kwargs):
        return self.cleaned_data
