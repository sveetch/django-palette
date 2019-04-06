import pytest
import json
import os

import django_palette
from django_palette.forms.source import SourceForm


@pytest.mark.parametrize("data,expected", [
    # source field is required
    (
        {"foo": "bar"},
        False,
    ),
    # source does not contain any valid color value
    (
        {"source": "bar"},
        False,
    ),
    # single color value
    (
        {"source": "#F0F0F0"},
        True,
    ),
    # multiple color values
    (
        {"source": "#F0F0F0\n#FF0000\n#000000"},
        True,
    ),
])
def test_required_fields(data, expected):
    """
    test validation
    """
    f = SourceForm(data)

    assert expected == f.is_valid()


@pytest.mark.parametrize("data,expected", [
    # source does not contain any valid color value
    (
        {"source": "bar"},
        [
            {
                "code": "invalid",
                "message": "Source does not contain any valid color value"
            }
        ],
    ),
    # one invalid hexadecimal length
    (
        {"source": "#ffffff #4444"},
        [
            {
                "code": "invalid",
                "message":  ("Source does contain some invalid color values, "
                             "ensure they are all on 3 or 6 hex "
                             "digit: #4444")
            }
        ],
    ),
    # many invalid hexadecimal length
    (
        {"source": "#1 #22 #333 #4444 #55555 #666666"},
        [
            {
                "code": "invalid",
                "message":  ("Source does contain some invalid color values, "
                             "ensure they are all on 3 or 6 hex "
                             "digit: #4444, #55555")
            }
        ],
    ),
])
def test_error_message(data, expected):
    """
    test returned source field error
    """
    f = SourceForm(data)
    f.is_valid()

    errors = json.loads(f.errors.as_json())
    msg = errors.get("source", None)

    assert expected == msg


@pytest.mark.parametrize("data,expected", [
    # single color value
    (
        {"source": "#F0F0F0"},
        {
            "#f0f0f0": [
                ("grey94", "#f0f0f0"),
                ('white', '#ffffff')
            ],
        },
    ),
    # multiple color values
    (
        {"source": "#F0F0F0\n#FF0000\n#000000"},
        {
            "#f0f0f0": [
                ("grey94", "#f0f0f0"),
                ('white', '#ffffff')
            ],
            "#ff0000": [
                ('red1', '#ff0000'),
                ('scarlet', '#fc2847')
            ],
            "#000000": [
                ('black', '#000000'),
                ('black', '#000000')
            ],
        },
    ),
    # multiple color values with duplications
    (
        {"source": "#F0F0F0\n#FF0000\n#F0F0F0\n#FF0000\n#000000"},
        {
            "#f0f0f0": [
                ("grey94", "#f0f0f0"),
                ('white', '#ffffff')
            ],
            "#ff0000": [
                ('red1', '#ff0000'),
                ('scarlet', '#fc2847')
            ],
            "#000000": [
                ('black', '#000000'),
                ('black', '#000000')
            ]
        },
    ),
])
def test_results(testsettings, settings, data, expected):
    """
    test returned success results
    """
    # Mock available registries for a lighter list
    settings.PALETTE_AVAILABLE_REGISTRIES = testsettings.available_registries

    f = SourceForm(data)
    f.is_valid()

    results = f.save()

    assert expected == results
