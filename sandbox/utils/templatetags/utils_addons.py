# -*- coding: utf-8 -*-
"""
Various usefull tags
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def googlefont(*fonts):
    """
    Produces a tag to request font families given as arguments.

    Each argument is assumed to be a valid family name and properties.

    Sample usage: ::

        {% googlefont "Open+Sans" %}
        {% googlefont "Open+Sans:300,400,700" %}
        {% googlefont "Open+Sans:300" "Railway:400,700" %}
        {% googlefont "Open+Sans:300" "Railway:400" "Roboto:900" %}

    """
    families = "%7C".join(fonts)
    return mark_safe(('<link href="//fonts.googleapis.com/css?family={}" '
                      'rel="stylesheet" type="text/css">').format(families))
