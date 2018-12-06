# -*- coding: utf-8 -*-
import os

import pytest

from django_palette.colors.registry import ColorRegistry


@pytest.mark.parametrize("registry_sample,expected_names,expected_hexas", [
    (
        [
            ('foo', '#ffffff'),
            ('bar', '#c0c0c0'),
            ('ping', '#ff0000'),
            ('pong', '#00ff00'),
            ('thing', '#808080'),
            ('mizzi', '#dd8014'),
            ('mizza', '#b4f345'),
        ],
        [
            ('foo', '#ffffff'),
            ('bar', '#c0c0c0'),
            ('ping', '#ff0000'),
            ('pong', '#00ff00'),
            ('thing', '#808080'),
            ('mizzi', '#dd8014'),
            ('mizza', '#b4f345'),
        ],
        [
            ('#ffffff', 'foo'),
            ('#c0c0c0', 'bar'),
            ('#ff0000', 'ping'),
            ('#00ff00', 'pong'),
            ('#808080', 'thing'),
            ('#dd8014', 'mizzi'),
            ('#b4f345', 'mizza'),
        ],
    ),
])
def test_get_registry_maps(registry_sample, expected_names, expected_hexas):
    """
    Testing names map has been correctly loaded
    """
    registry = ColorRegistry()
    registry.load()

    names, hexas = registry.get_registry_maps(registry_sample)

    assert names == expected_names

    assert hexas == expected_hexas


def test_loading():
    """
    Testing names map has been correctly loaded
    """
    registry = ColorRegistry()
    registry.load()

    assert ('black' in dict(registry.name_map)) == True
    assert ('white' in dict(registry.name_map)) == True
    assert ('#000000' in dict(registry.hexa_map)) == True
    assert ('#ffffff' in dict(registry.hexa_map)) == True

    assert ('foo' in dict(registry.name_map)) == False
    assert ('#foo' in dict(registry.hexa_map)) == False
