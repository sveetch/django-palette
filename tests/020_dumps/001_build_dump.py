import pytest

from django.conf import settings
from django_palette.dumps import build_dump


@pytest.mark.parametrize("format_key,expected", [
    (
        "json",
        (
            '''{\n'''
            '    "white": "#ffffff",\n'''
            '    "black": "#000000"\n'
            '}\n'
        )
    ),
])
def test_dump_format_opts(format_key, expected):
    """
    Build dump giving format key name and format options dict
    """
    data = [
        {
            "color":"#ffffff", "name": "white"
        },
        {
            "color":"#000000", "name": "black"
        },
    ]

    format_opts = settings.PALETTE_DUMP_FORMATS[format_key]

    output = build_dump(format_key, data, opts=format_opts)

    assert output["content"] == expected


@pytest.mark.parametrize("format_key,expected", [
    (
        "json",
        (
            "{\n"
            "    \"white\": \"#ffffff\",\n"
            "    \"black\": \"#000000\"\n"
            "}\n"
        )
    ),
    (
        "scss-vars",
        (
            "// Colors\n"
            "$white: #ffffff;\n"
            "$black: #000000;\n\n"
        )
    ),
    (
        "python-dict",
        (
            "palette = {\n"
            "    \"white\": \"#ffffff\",\n"
            "    \"black\": \"#000000\"\n"
            "}\n"
        )
    ),
    (
        "html-snippet",
        (
            "<style>\n"
            ".djangopalette-dump{\n"
            "    display: flex;\n"
            "    flex-direction: row;\n"
            "    flex-wrap: wrap;\n"
            "}\n"
            ".djangopalette-dump .item{\n"
            "    flex: 1 0 20%;\n"
            "    max-width: 20%;\n"
            "    padding: 8px;\n"
            "}\n"
            ".djangopalette-dump .item .color{\n"
            "    width: 100%;\n"
            "    height: 48px;\n"
            "}\n"
            "</style>\n"
            "<div class=\"djangopalette-dump\">\n"
            "  <div class=\"item\">\n"
            "    <div class=\"color\" style=\"background-color: #ffffff;\"></div>\n"
            "    <p class=\"code\">#ffffff</p>\n"
            "    <p class=\"name\">white</p>\n"
            "  </div><div class=\"item\">\n"
            "    <div class=\"color\" style=\"background-color: #000000;\"></div>\n"
            "    <p class=\"code\">#000000</p>\n"
            "    <p class=\"name\">black</p>\n"
            "  </div>\n"
            "</div>\n"
        )
    ),
])
def test_dump_all_formats(format_key, expected):
    """
    This should test against every available format
    """
    data = [
        {
            "color":"#ffffff", "name": "white"
        },
        {
            "color":"#000000", "name": "black"
        },
    ]
    output = build_dump(format_key, data)

    assert output["content"] == expected
