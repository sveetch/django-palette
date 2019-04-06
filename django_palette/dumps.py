from django.conf import settings
from django.template import loader


def build_dump(key, data, opts=None, extra_context={}):
    """
    Build dump format from given data
    """
    opts = opts or settings.PALETTE_DUMP_FORMATS[key]

    context = {
        "format_key": key,
        "format_name": opts["name"],
        "palette": data,
    }
    context.update(extra_context)

    template = loader.get_template(opts["template"])

    return {
        "key": key,
        "name": opts["name"],
        "content": template.render(context),
    }
