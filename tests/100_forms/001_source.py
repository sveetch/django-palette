import pytest
import json

from django_palette.forms.source import SourceForm


@pytest.mark.parametrize('data,expected', [
    # source field is required
    (
        {'foo': 'bar'},
        False,
    ),
    # source does not contain any valid color value
    (
        {'source': 'bar'},
        False,
    ),
    # single color value
    (
        {'source': '#F0F0F0'},
        True,
    ),
    # multiple color values
    (
        {'source': '#F0F0F0\n#FF0000\n#000000'},
        True,
    ),
])
def test_required_fields(data, expected):
    """
    test validation
    """
    f = SourceForm(data)

    assert expected == f.is_valid()


def test_error_message():
    """
    test returned message error
    """
    f = SourceForm({'source': 'bar'})
    f.is_valid()

    errors = json.loads(f.errors.as_json())
    msg = errors.get('source', None)

    expected = [
        {
            "code": "invalid",
            "message": "Source does not contain any valid color value"
        }
    ]

    assert expected == msg


@pytest.mark.parametrize('data,expected', [
    # single color value
    (
        {'source': '#F0F0F0'},
        {
            '#f0f0f0': [('gray94', '#f0f0f0')],
        },
    ),
    # multiple color values
    (
        {'source': '#F0F0F0\n#FF0000\n#000000'},
        {
            '#f0f0f0': [('gray94', '#f0f0f0')],
            '#ff0000': [('red1', '#ff0000')],
            '#000000': [('black', '#000000')],
        },
    ),
    # multiple color values with duplications
    (
        {'source': '#F0F0F0\n#FF0000\n#F0F0F0\n#FF0000\n#000000'},
        {
            '#f0f0f0': [('gray94', '#f0f0f0')],
            '#ff0000': [('red1', '#ff0000')],
            '#000000': [('black', '#000000')]
        },
    ),
])
def test_results(data, expected):
    """
    test returned success results
    """
    f = SourceForm(data)
    f.is_valid()

    results = f.save()

    assert expected == results
