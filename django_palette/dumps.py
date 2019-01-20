from django.template import RequestContext, loader


def build_dump(key, format_opts, data, extra_context={}):
    """
    Build dump format from given data
    """
    output = ""

    context = {
        "format_key": key,
        "format_name": format_opts["name"],
        "palette": data,
    }
    context.update(extra_context)

    template = loader.get_template(format_opts["template"])

    return template.render(context)
