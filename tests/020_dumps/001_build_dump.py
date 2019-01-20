import pytest

from django.conf import settings
from django_palette.dumps import build_dump


@pytest.mark.parametrize("data,format_key", [
    # valid single element
    (
        [
            {
                "color":"#ffffff", "name": "white"
            },
            {
                "color":"#000000", "name": "black"
            },
        ],
        "json",
    ),
    # valid single element
    (
        [
            {
                "color":"#ffffff", "name": "white"
            },
            {
                "color":"#000000", "name": "black"
            },
        ],
        "scss-vars",
    ),
])
def test_dump(data, format_key):
    format_opts = settings.PALETTE_DUMP_FORMATS[format_key]

    output = build_dump(format_key, format_opts, data)

    print("==== Format {} ====".format(format_key))
    print(output)
    print()

    assert output == 42
