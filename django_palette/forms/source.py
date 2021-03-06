from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_palette.colors.finder import ColorFinder
from django_palette.colors.naming import ColorNames


class SourceForm(forms.Form):
    """
    Form to get named color palette from given source content
    """
    source = forms.CharField(
        label=_("Source"),
        widget=forms.Textarea,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.colors = {}
        self.registries = self.get_registries()

        super(SourceForm, self).__init__(*args, **kwargs)

    def get_registries(self, *args, **kwargs):
        namers = []

        for name, path in settings.PALETTE_AVAILABLE_REGISTRIES:
            namer = ColorNames()
            namer.load(path=path)
            namers.append(namer)

        return namers

    def store_colors(self, store, palette):
        """
        Store found name suggestion for palette colors.

        It should be almost ready to store multiple color name suggestions
        from different registry.
        """
        for k, v in palette.items():
            if k not in store:
                store[k] = []
            store[k].append(v)

        return store

    def clean_source(self):
        """
        Validate source contains valid colors then compute named color palette
        in ``SourceForm.colors`` attribute.
        """
        source = self.cleaned_data.get("source")

        if source:
            finder = ColorFinder()
            colors = finder.find(source)

            if not colors:
                raise ValidationError(
                    _("Source does not contain any valid color value"),
                    code='invalid',
                )

            # Ensure hex colors lengths
            length_errors = []
            for item in colors:
                if item.startswith("#"):
                    if len(item[1:]) > 3 and len(item[1:]) < 6:
                        length_errors.append(item)

            if length_errors:
                errors = ", ".join(sorted(length_errors))
                raise ValidationError(
                    _("Source does contain some invalid color values, ensure "
                      "they are all on 3 or 6 hex digit: {}").format(errors),
                    code='invalid',
                )

            # Update color store from registries
            for namer_registry in self.registries:
                self.colors = self.store_colors(self.colors,
                                                namer_registry.batch(colors))

        return source

    def save(self, *args, **kwargs):
        return self.colors
