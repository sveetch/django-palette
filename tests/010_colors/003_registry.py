# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

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
        OrderedDict([
            ('foo', '#ffffff'),
            ('bar', '#c0c0c0'),
            ('ping', '#ff0000'),
            ('pong', '#00ff00'),
            ('thing', '#808080'),
            ('mizzi', '#dd8014'),
            ('mizza', '#b4f345'),
        ]),
        OrderedDict([
            ('#ffffff', 'foo'),
            ('#c0c0c0', 'bar'),
            ('#ff0000', 'ping'),
            ('#00ff00', 'pong'),
            ('#808080', 'thing'),
            ('#dd8014', 'mizzi'),
            ('#b4f345', 'mizza'),
        ]),
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


def test_source_loading():
    """
    Testing names map has been correctly loaded from given map iterable.
    """
    registry = ColorRegistry()
    registry.load(names=[
        ('ping', '#00ff00'),
        ('pong', '#c0c0c0'),
        ('pang', '#ff0000'),
        ('black', '#000000'),
    ])

    assert ('ping' in registry.name_map) == True
    assert ('pong' in registry.name_map) == True
    assert ('#ff0000' in registry.hexa_map) == True
    assert ('#000000' in registry.hexa_map) == True

    assert ('white' in registry.name_map) == False
    assert ('#ffffff' in registry.hexa_map) == False


def test_file_loading():
    """
    Testing names map has been correctly loaded from default map file.
    """
    registry = ColorRegistry()
    registry.load()

    assert ('black' in registry.name_map) == True
    assert ('white' in registry.name_map) == True
    assert ('#000000' in registry.hexa_map) == True
    assert ('#ffffff' in registry.hexa_map) == True

    assert ('foo' in registry.name_map) == False
    assert ('#foo' in registry.hexa_map) == False
