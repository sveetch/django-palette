# -*- coding: utf-8 -*-
import os

import pytest

from django_palette.colors.naming import validate_name


@pytest.mark.parametrize("name,expected", [
    (
        "#000000", False
    ),
    (
        "foo", True
    ),
    (
        "fooé", False
    ),
    (
        "fooo¢", False
    ),
    (
        "foo bar", False
    ),
    (
        "foo-bar", True
    ),
    (
        "foo_bar", True
    ),
    (
        "foo-bar_ping42", True
    ),
    (
        "-foobar", False
    ),
    (
        "_foobar", False
    ),
])
def test_nearest_color_name(name, expected):
    """
    Testing name validation
    """
    assert validate_name(name) == expected
