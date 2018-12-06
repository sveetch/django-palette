# -*- coding: utf-8 -*-
import os

import pytest

from django_palette.colors.naming import ColorNames


@pytest.mark.parametrize("color,expected", [
    (
        "#000000",
        ("black", "#000000"),
    ),
    (
        "#ff0000",
        ("red1", "#ff0000"),
    ),
    (
        "#8461a1",
        ("plum4", "#8b668b"),
    ),
    (
        "#602f8a",
        ("darkorchid4", "#68228b"),
    ),
    (
        "#b29e6b",
        ("darkkhaki", "#bdb76b"),
    ),
    (
        "#505050",
        ("gray31", "#4f4f4f"),
    ),
    (
        "#40b59b",
        ("mediumseagreen", "#3cb371"),
    ),
    (
        "#00688b",
        ("deepskyblue4", "#00688b"),
    ),
    (
        "#f7f5f2",
        ("whitesmoke", "#f5f5f5"),
    ),
])
def test_nearest_color_name(color, expected):
    """
    Testing nearest color name finder is accurate
    """
    namer = ColorNames()
    namer.load()

    assert namer.nearest_color_name(color) == expected


@pytest.mark.parametrize("colors,expected", [
    (
        ["#000000", "#ff0000"],
        {
            "#000000": ("black", "#000000"),
            "#ff0000": ("red1", "#ff0000"),
        }
    ),
    (
        ["#8461a1", "#602f8a", "#505050"],
        {
            "#8461a1": ("plum4", "#8b668b"),
            "#602f8a": ("darkorchid4", "#68228b"),
            "#505050": ("gray31", "#4f4f4f"),
        }
    ),
    (
        ['#cb432b', '#7db828', '#013b61', '#17436a', '#59758d', '#ecebe9',
         '#e0e0e0'],
        {
            '#013b61': ('midnightblue', '#191970'),
            '#17436a': ('midnightblue', '#191970'),
            '#59758d': ('lightskyblue4', '#607b8b'),
            '#7db828': ('yellowgreen', '#9acd32'),
            '#cb432b': ('brown3', '#cd3333'),
            '#e0e0e0': ('gray88', '#e0e0e0'),
            '#ecebe9': ('gray92', '#ebebeb')
        }
    ),
])
def test_batch_names(colors, expected):
    """
    Testing nearest color name finder is accurate
    """
    namer = ColorNames()
    namer.load()

    assert namer.batch_names(colors) == expected


@pytest.mark.xfail(raises=AssertionError)
def test_naming_flaw():
    """
    A test expected to fail

    It demonstrate a flaw in naming that result to return the same color name
    for different colors.

    This would be a nice feature to avoid this with smart naming,
    counting the same color name and numerotate names after. Problem is it
    would result to red1, red2, etc.. for the same 'red' name, but a red2 name
    can allready exists in registry and leading so to have duplicate red2 names.
    """
    colors = [
        '#cb432b', '#7db828', '#013b61', '#17436a', '#59758d', '#ecebe9',
        '#e0e0e0'
    ]

    expected = {
        '#013b61': ('midnightblue', '#191970'),
        '#17436a': ('midnightblue2', '#191970'),
        '#59758d': ('lightskyblue4', '#607b8b'),
        '#7db828': ('yellowgreen', '#9acd32'),
        '#cb432b': ('brown3', '#cd3333'),
        '#e0e0e0': ('gray88', '#e0e0e0'),
        '#ecebe9': ('gray92', '#ebebeb')
    }

    namer = ColorNames()
    namer.load()

    assert namer.batch_names(colors) == expected
