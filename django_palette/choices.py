from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Special palette color value to watch for custom name input
PALETTE_NAME_CUSTOM = "other"


# Palette base choices contains required items that allways stand at the end
# of choices
PALETTEITEM_BASE_CHOICES = [
    (PALETTE_NAME_CUSTOM, _("Other")),
]


# Enabled dump format choices
DUMP_FORMATS_CHOICES = [
    (k, v["name"]) for k, v in settings.PALETTE_DUMP_FORMATS.items()
]
