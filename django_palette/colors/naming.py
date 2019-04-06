# -*- coding: utf-8 -*-
from string import ascii_lowercase, digits

from colour import Color

from django_palette.colors import toCssRGB
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
    """
    Color name finder.

    Using a registry to find a nearest color name if no exact value match a
    color from registered names.

    Arguments:
        **kwargs: ``enable_modifier``, ``grey_bonus``, ``grey_malus`` and
            ``avoid_twice`` attribute values can be passed as kwargs.

    Atributes:
        enable_modifier (bool): Enable modifier when calculating color
            difference when searching for nearest value. The modifier is
            either a bonus or a malus to avoid using grey color name for non
            grey color. Enabled by default.
        grey_bonus (int): An integer to subtract on calculated difference when
            searched color and confronted color are both grey.
        grey_malus (int): An integer to add on calculated difference when
            searched color is not grey but confronted color is.
        avoid_twice (bool): Enable feature to avoid using a color name that
            has already be used before for a previous color.
        used_colors (dict): A dictionnary that store already used color name.
    """
    def __init__(self, *args, **kwargs):
        self.enable_modifier = kwargs.pop("enable_modifier", True)
        self.grey_bonus = kwargs.pop("grey_bonus", 30000)  # Around 15%
        self.grey_malus = kwargs.pop("grey_malus", 15000)  # Around 7.5%
        self.avoid_twice = kwargs.pop("avoid_twice", True)

        super().__init__(*args, **kwargs)

        self.used_colors = {}

    def is_grey(self, red, green, blue):
        """
        Shortcut to find if rgb values correspond to grey color, such as red,
        green and blues values are equal. White and black colors are assumed to
        be a grey color.

        NOTE:
            * Maybe added instead to Color extension as a "get property";
            * OR Should accept a Color object argument instead of rgb value
              arguments.

        Args:
            red (int): Integer value from 0 to 255 for red.
            green (int): Integer value from 0 to 255 for green.
            blue (int): Integer value from 0 to 255 for blue.

        Returns:
            bool: True if rgb values correspond to a grey color, else False.
        """
        return (red == green == blue)

    def store_used_color(self, name, hexa):
        """
        Store given color in a registry about used color stats.

        Args:
            hexa (str): Long hexadecimal color code.
            name (str): Color name.

        Returns:
            int: An integer to represent usage count for given color.
        """
        if name not in self.used_colors:
            self.used_colors[name] = {
                "hexa": hexa,
                "count": 1,
            }
        else:
            self.used_colors[name]["count"] += 1

        return self.used_colors[name]["count"]

    def calculate_diff(self, searched_rgb, searched_isgrey, confronted_color):
        """
        Try to find an exact match from registry for given color.

        Args:
            searched_rgb (tuple): RGB value to search difference from.
            searched_isgrey (bool): If searched color is grey or not.
            confronted_color (colour.Color): Color that is confronted to the
                searched one.

        Returns:
            tuple: diff, bonus, malus
        """
        searched_red, searched_green, searched_blue = searched_rgb

        r, g, b = toCssRGB(confronted_color.rgb)

        isgrey = self.is_grey(r, g, b)

        # Compute RGB values difference between searched and confronted
        diff = (abs(searched_red - r) * 256) + \
               (abs(searched_green - g) * 256) + \
               (abs(searched_blue - b) * 256)

        bonus = False
        malus = False
        # Apply bonus/malus grey modifier if enabled
        if self.enable_modifier:
            if searched_isgrey and isgrey:
                bonus = True
                diff = diff - self.grey_bonus
            elif not searched_isgrey and isgrey:
                malus = True
                diff = diff + self.grey_malus

        return (diff, bonus, malus)

    def job_exact_match(self, color):
        """
        Try to find an exact match from registry for given color.

        Args:
            color (colour.Color): Color object.

        Returns:
            tuple: A tuple of (name, hexadecimal)
        """
        if color.hex_l in self.hexa_map:
            return (self.hexa_map[color.hex_l], color.hex_l.lower())

        return None

    def job_nearest_match(self, color, ignore=[]):
        """
        Try to find a nearest match from registry for given color.

        The minimum diff is 0 and maximum is 195840 (aka: 255*256*3).

        Args:
            color (colour.Color): Color object.
            ignore (list): Hexadecimal code to ignore for match.

        Returns:
            tuple: A tuple of (name, hexadecimal) or ``None`` if no name has
            been finded.
        """
        min_diff = None
        found_name = found_hexa = None
        searched_red, searched_green, searched_blue = toCssRGB(color.rgb)
        searched_isgrey = self.is_grey(searched_red, searched_green, searched_blue)

        for available_hexa, available_name in self.hexa_map.items():
            if available_hexa in ignore:
                continue
            elif self.avoid_twice and available_name in self.used_colors:
                continue

            # Calculate difference
            diff, bonus, malus = self.calculate_diff(
                (searched_red, searched_green, searched_blue),
                searched_isgrey,
                Color(available_hexa)
            )

            # Memorize color with a lower difference
            if min_diff is None or diff < min_diff:
                min_diff = diff
                found_name = available_name
                found_hexa = available_hexa.lower()

        if not found_hexa:
            return None

        return (found_name, found_hexa)

    def find(self, hexa, ignore=[]):
        """
        Find a name from registry for given hexadecimal color.

        Args:
            hexa (str): Long hexadecimal color code like ``#000000``, not
                short code like ``#000``.
            ignore (list): Hexadecimal codes to ignore from registry.

        Returns:
            tuple: A tuple of (name, hexadecimal)
        """
        color = Color(hexa)

        exact_match = self.job_exact_match(color)
        if exact_match:
            self.store_used_color(*exact_match)
            return exact_match

        nearest_match = self.job_nearest_match(color, ignore=ignore)
        self.store_used_color(*nearest_match)

        return nearest_match

    def batch(self, hexas, ignore=[]):
        """
        Find a name from registry for every given hexadecimal colors.

        Similar to ``ColorNames.find()`` method but try to find an exact match
        before nearest match batch in different loops to ensure exact name
        match are not stealed by a previous nearest match.

        Args:
            hexas (list): List of long hexadecimal color codes like
                ``#000000``.
            ignore (list): Hexadecimal codes to ignore from registry.

        Returns:
            list: List of tuples of (name, hexadecimal).
        """
        matchs = {}

        # Sort given codes so they are ordered from darker to lightest
        hexas = sorted(hexas)

        # Firstly loop preserve all exact match
        for code in hexas:
            color = Color(code)

            exact_match = self.job_exact_match(color)
            if exact_match:
                self.store_used_color(*exact_match)
                matchs[code] = exact_match

        # Then nearest match for every other values
        for code in hexas:
            if code not in matchs:
                color = Color(code)
                nearest_match = self.job_nearest_match(color, ignore=ignore)
                matchs[code] = nearest_match
                self.store_used_color(*nearest_match)

        return matchs
