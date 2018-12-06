# -*- coding: utf-8 -*-
import pytest

from colour import Color

from django_palette.colors import toColourRGB, toCssRGB


@pytest.mark.parametrize("hexa,rgb_int", [
    # red
    (
        "#ff0000",
        (255, 0, 0),
    ),
    # black
    (
        "#000000",
        (0, 0, 0),
    ),
    # white
    (
        "#ffffff",
        (255, 255, 255),
    ),
    # blue facebook
    (
        "#4267b2",
        (66, 103, 178),
    ),
    # light pink
    (
        "#fce3e3",
        (252, 227, 227),
    ),
    # light pastel yellow
    (
        "#fdffdf",
        (253, 255, 223),
    ),
    # purple
    (
        "#8938aa",
        (137, 56, 170),
    ),
    # green grass
    (
        "#53a93f",
        (83, 169, 63),
    ),
])
def test_toColourRGB(hexa, rgb_int):
    """
    Test rgb value conversion from integer to float is correct using long
    hexadecimal to compare
    """
    clr = Color(hexa)

    rgb_floats = toColourRGB(rgb_int)

    assert hexa == Color(rgb=rgb_floats).hex_l


@pytest.mark.parametrize("hexa,rgb_int,rgb_float", [
    # red
    (
        "#ff0000",
        (255, 0, 0),
        (1.0, 0.0, 0.0),
    ),
    # black
    (
        "#000000",
        (0, 0, 0),
        (0.0, 0.0, 0.0),
    ),
    # white
    (
        "#ffffff",
        (255, 255, 255),
        (1.0, 1.0, 1.0),
    ),
    # blue facebook
    (
        "#4267b2",
        (66, 103, 178),
        (0.25882352941176473, 0.403921568627451, 0.6980392156862745),
    ),
    # light pink
    (
        "#fce3e3",
        (252, 227, 227),
        (0.9882352941176471, 0.8901960784313725, 0.8901960784313725),
    ),
    # light pastel yellow
    (
        "#fdffdf",
        (253, 255, 223),
        (0.9921568627450981, 1.0, 0.8745098039215686),
    ),
    # purple
    (
        "#8938aa",
        (137, 56, 170),
        (0.5372549019607843, 0.2196078431372549, 0.6666666666666666),
    ),
    # green grass
    (
        "#53a93f",
        (83, 169, 63),
        (0.3254901960784314, 0.6627450980392157, 0.24705882352941178),
    ),
])
def test_toCssRGB(hexa, rgb_int, rgb_float):
    """
    Test rgb value conversion from integer to float is correct
    """
    # Compare attempt integers to converted float to int
    assert rgb_int == toCssRGB(rgb_float)
