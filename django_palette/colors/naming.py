# -*- coding: utf-8 -*-
"""
* When a color name is used more than one time, increment names with "_[+1]" for all other identic names;
"""
import json, os, re
from string import ascii_lowercase, digits

from pathlib import Path

from colour import Color

from django_palette.colors import toColourRGB, toCssRGB
from django_palette.colors.registry import ColorRegistry
from django_palette.colors.dumper import ColorDump


ALLOWED_COLORNAME_CHARACTERS = ascii_lowercase + digits + "_-"


def validate_name(content):
    """
    Validate a color name.

    Only ascii lowercase alphabet characters, digits, ``_`` and ``-``.

    Args:
        content (str): Name to validate.

    Returns:
        bool: ``True`` if name is valid else ``False``.
    """
    if content.startswith("_") or content.startswith("-"):
        return False

    for item in content:
        if item not in ALLOWED_COLORNAME_CHARACTERS:
            return False

    return True


class ColorNames(ColorDump, ColorRegistry):
    def nearest_color_name(self, hexa):
        """
        Find nearest color name from color name registry.

        Nearest color is found through a difference from given color and
        available name colors.

        Difference is computed by adding up RGB values and compare it to each
        added up RGB value from available name colors. In the end of scanning
        name colors, the lesser difference win.

        Args:
            hexa (str): Long hexadecimal color code like ``#000000``, not
                short code like ``#000``.

        Returns:
            tuple: A tuple of nearest color name and its original hexadecimal
            code than can differ from given ``hexa`` argument. If no color
            has been finded, return ``None``. hexadecimal code are allways
            lowercase.
        """
        min_diff = None
        searched_color = Color(hexa)
        searched_red, searched_green, searched_blue = toCssRGB(searched_color.rgb)
        color_name = original_hex = None

        for available_hexa, available_name in self.hexa_map:
            r, g, b = toCssRGB(Color(available_hexa).rgb)

            # Compute RGB values difference between colors
            diff = (abs(searched_red - r) * 256) + \
                    (abs(searched_green - g) * 256) + \
                    (abs(searched_blue- b) * 256)

            if min_diff is None or diff < min_diff:
                min_diff = diff
                color_name = available_name
                original_hex = available_hexa

        return (color_name, original_hex.lower())

    def batch_names(self, colors):
        """
        Find nearest color names for every given hexadecimal codes.

        Args:
            colors (list): List of long hexadecimal color code.

        Returns:
            dict: A dictionnary of given colors with their nearest color name.
            Color key are allways lowercase.
        """
        batchs = {}

        for code in colors:
            found = self.nearest_color_name(code)
            if found[0] is not None:
                batchs[code.lower()] = found

        return batchs
