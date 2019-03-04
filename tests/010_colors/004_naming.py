# -*- coding: utf-8 -*-
import os

import pytest

from colour import Color

from django_palette.colors.naming import ColorNames


# Lightweight registry for tests
DUMMY_REGISTRY = [
    ("gray83", "#d4d4d4"),
    ("gray25", "#404040"),
    ("gray22", "#383838"),
    ("gray13", "#212121"),
    ("gray14", "#242424"),
    ("white", "#ffffff"),
    ("red1", "#ff0000"),
    ("red2", "#ee0000"),
    ("black", "#000000"),
    ("yellowgreen", "#9acd32"),
    ("brown3", "#cd3333"),
    ("midnightblue", "#191970"),
]


@pytest.mark.parametrize("rgb,expected", [
    (
        (0, 0, 0),
        True,
    ),
    (
        (255, 255, 255),
        True,
    ),
    (
        (42, 42, 42),
        True,
    ),
    (
        (41, 42, 42),
        False,
    ),
    (
        (42, 42, 41),
        False,
    ),
    (
        (41, 42, 43),
        False,
    ),
    (
        (0, 255, 7),
        False,
    ),
])
def test_is_grey(rgb, expected):
    """
    Testing if rgb value is a grey tone
    """
    namer = ColorNames()

    assert namer.is_grey(*rgb) == expected


@pytest.mark.parametrize("hexa,expected", [
    (
        "#ffffff",
        ("white", "#ffffff"),
    ),
    (
        "#404040",
        ("gray25", "#404040"),
    ),
    (
        "#404041",
        None,
    ),
    (
        "#123456",
        None,
    ),
])
def test_job_exact_match(hexa, expected):
    """
    Testing exact name matching job
    """
    namer = ColorNames()
    namer.load(names=DUMMY_REGISTRY)
    assert namer.job_exact_match(Color(hexa)) == expected


@pytest.mark.parametrize("pasts,current,expected", [
    (
        [],
        ("white", "#ffffff"),
        1,
    ),
    (
        [
            ("white", "#ffffff"),
        ],
        ("white", "#ffffff"),
        2,
    ),
    (
        [
            ("white", "#ffffff"),
            ("red1", "#ff0000"),
            ("white", "#ffffff"),
        ],
        ("white", "#ffffff"),
        3,
    ),
    (
        [
            ("red1", "#ff0000"),
            ("gray22", "#383838"),
            ("gray13", "#212121"),
        ],
        ("white", "#ffffff"),
        1,
    ),
])
def test_store_used_color(pasts, current, expected):
    """
    Check method return a correct counter and stats
    """
    namer = ColorNames()
    namer.load(names=[])

    # Quietly store some colors
    for item in pasts:
        namer.store_used_color(*item)

    # Assert on current color
    assert namer.store_used_color(*current) == expected


@pytest.mark.parametrize("hexa,ignored,expected", [
    (
        "#ffffff",
        [],
        ("white", "#ffffff"),
    ),
    # gray94 near white
    (
        "#f0f0f0",
        [],
        ("white", "#ffffff"),
    ),
    # cyan near gray14
    (
        "#0e242b",
        [],
        ("gray14", "#242424"),
    ),
    # lemon green near yellowgreen
    (
        "#7db828",
        [],
        ("yellowgreen", "#9acd32"),
    ),
    # some red near to brown3
    (
        "#cb432b",
        [],
        ("brown3", "#cd3333"),
    ),
    # gray94 near white, but white is ignored
    (
        "#f0f0f0",
        ["#ffffff"],
        ("gray83", "#d4d4d4"),
    ),
    # gray94 near white, but white and gray83 are ignored
    (
        "#f0f0f0",
        ["#ffffff", "#d4d4d4"],
        ("yellowgreen", "#9acd32"),
    ),
])
def test_job_nearest_match(hexa, ignored, expected):
    """
    Testing nearest name matching job
    """
    namer = ColorNames()
    namer.load(names=DUMMY_REGISTRY)
    #print("==== For {} ====".format(hexa))
    #print("ignored:", ignored)
    #print("expected:", expected)
    assert namer.job_nearest_match(Color(hexa), ignore=ignored) == expected
    #assert 1 == 42


@pytest.mark.parametrize("pasts,current,expected", [
    # Simple exact match
    (
        [],
        "#ffffff",
        ("white", "#ffffff"),
    ),
    # Exact match is not subject to ignore allready used value
    # This should be ok for single search with "find()"
    (
        [
            ("white", "#ffffff"),
        ],
        "#ffffff",
        ("white", "#ffffff"),
    ),
    # Nearest match
    (
        [
            ("red1", "#ff0000"),
        ],
        "#f0f0f0",
        ("white", "#ffffff"),
    ),
    # Nearest match
    (
        [
            ("red1", "#ff0000"),
            ("gray13", "#212121"),
        ],
        "#393939",
        ("gray22", "#383838"),
    ),
    # Would expect for gray22 but it has allready been used, so fallback to
    # gray25
    (
        [
            ("red1", "#ff0000"),
            ("gray22", "#383838"),
            ("gray13", "#212121"),
        ],
        "#393939",
        ("gray25", "#404040"),
    ),
    # Very nearest color is red1 but has allready be used, so fallback to
    # red2
    (
        [
            ("red1", "#ff0000"),
            ("gray22", "#383838"),
            ("gray13", "#212121"),
        ],
        "#ff0001",
        ("red2", "#ee0000"),
    ),
])
def test_find_basic(pasts, current, expected):
    """
    Testing single color name finding with dummy registry with some used color
    values
    """
    namer = ColorNames()
    namer.load(names=DUMMY_REGISTRY)

    # Quietly store some colors
    for item in pasts:
        namer.store_used_color(*item)

    # Assert on current color
    assert namer.find(current) == expected


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
        ("seashell1", "#fff5ee")
    ),
])
def test_find_accuracy(color, expected):
    """
    Testing single color name finding accuracy with default registry
    """
    namer = ColorNames()
    namer.load()

    assert namer.find(color) == expected


@pytest.mark.parametrize("colors,expected", [
    # Basic exact match
    (
        ["#000000", "#ff0000"],
        {
            "#000000": ("black", "#000000"),
            "#ff0000": ("red1", "#ff0000"),
        }
    ),
    # Same values does not perform two different matchs
    (
        ["#000000", "#ff0000", "#ff0000"],
        {
            "#000000": ("black", "#000000"),
            "#ff0000": ("red1", "#ff0000"),
        }
    ),
    # Differents colors does not match to the same name and previous nearest
    # color does not predates following exact match
    (
        ["#013b61", "#191970", "#17436a"],
        {
            "#013b61": ("gray22", "#383838"),
            "#191970": ("midnightblue", "#191970"),
            "#17436a": ("gray25", "#404040"),
        }
    ),
])
def test_batch_names_basic(colors, expected):
    """
    Testing name finding for a batch of colors with dummy registry
    """
    namer = ColorNames()
    namer.load(names=DUMMY_REGISTRY)

    assert namer.batch(colors) == expected


@pytest.mark.parametrize("colors,expected", [
    (
        [
            "#000000",
            "#ffffff",
            "#404040",
            "#fefefe",
            "#022e4b",
            "#0a507c",
            "#1689b9",
            "#edf8ff",
            "#38393d",
            "#b5b8c4",
            "#f3f5fb",
        ],
        {
            "#000000": ("black", "#000000"),
            "#ffffff": ("white", "#ffffff"),
            "#404040": ("gray25", "#404040"),
            "#fefefe": ("gray99", "#fcfcfc"),
            "#022e4b": ("midnightblue", "#191970"),
            "#0a507c": ("dodgerblue4", "#104e8b"),
            "#1689b9": ("dodgerblue3", "#1874cd"),
            "#edf8ff": ("aliceblue", "#f0f8ff"),
            "#38393d": ("darkslategray", "#2f4f4f"),
            "#b5b8c4": ("lightcyan3", "#b4cdcd"),
            "#f3f5fb": ("mintcream", "#f5fffa"),
        }
    ),
    (
        [
            "#cb432b",
            "#7db828",
            "#013b61",
            "#17436a",
            "#59758d",
            "#ecebe9",
            "#e0e0e0",
        ],
        {
            "#013b61": ("midnightblue", "#191970"),
            "#17436a": ("dodgerblue4", "#104e8b"),
            "#59758d": ("lightskyblue4", "#607b8b"),
            "#7db828": ("yellowgreen", "#9acd32"),
            "#cb432b": ("brown3", "#cd3333"),
            "#e0e0e0": ("gray88", "#e0e0e0"),
            "#ecebe9": ("snow2", "#eee9e9"),
        }
    ),
])
def test_batch_names_accuracy(colors, expected):
    """
    Testing name finding for a batch of colors with default registry

    This should ensure match accuracy with default algorithm (bonus/malus with
    greys, exact match and no twice values)
    """
    namer = ColorNames()
    namer.load()

    assert namer.batch(colors) == expected
