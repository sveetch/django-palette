import json

import pytest

from django.urls import reverse


def test_get_notallowed(client):
    """
    Source post view should return an http405 since it does not accept GET
    """
    url = reverse('django_palette:dump-post')
    response = client.get(url)
    assert response.status_code == 405


@pytest.mark.parametrize("data,expected", [
    # Every fields required but not any one given
    (
        {
            'wrong': 'nope',
        },
        {
            'formats': ['This field is required.'],
            'palette': ['This field is required.'],
        },
    ),
    # Palette is empty
    (
        {
            "palette": "",
            "formats": ["json"],
        },
        {
            'palette': ['This field is required.'],
        }
    ),
    # Palette JSON is an empty list
    (
        {
            "palette": "[]",
            "formats": ["json"],
        },
        {
            'palette': ['This field is required.'],
        }
    ),
    # Palette JSON is invalid JSON
    (
        {
            "palette": "nope",
            "formats": ["json"],
        },
        {
            'palette': ['Invalid JSON data.'],
        }
    ),
    # Palette JSON is invalid structure (dict instead of list)
    (
        {
            "palette": json.dumps({"color": "bar", "name": "bar"}),
            "formats": ["json"],
        },
        {
            'palette': ['Palette data structure is invalid.'],
        }
    ),
    # Palette items have invalid structure (missing fields)
    (
        {
            "palette": json.dumps([{"color": "bar"}]),
            "formats": ["json"],
        },
        {
            'palette': ['Palette data structure is invalid.'],
        }
    ),
    # Format value got a single invalid value
    (
        {
            "palette": json.dumps([{"color": "bar", "name": "foo"}]),
            "formats": ["nope"],
        },
        {
            'formats': ["Select a valid choice. nope is not one of the "
                        "available choices."],
        }
    ),
    # Format value got invalid value in many choices
    (
        {
            "palette": json.dumps([{"color": "bar", "name": "foo"}]),
            "formats": ["boo", "json"],
        },
        {
            'formats': ["Select a valid choice. boo is not one of the "
                        "available choices."],
        }
    ),
])
def test_post_error(client, data, expected):
    """
    On error, palette post view should return a http400 with correct message
    in JSON
    """
    url = reverse('django_palette:dump-post')

    response = client.post(
        url,
        json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == 400

    content_json = json.loads(response.content.decode('utf-8'))
    assert content_json.get('data') == expected


@pytest.mark.parametrize("data,expected_palette", [
    (
        {
            "palette": json.dumps([{"color": "bar", "name": "foo"}]),
            "formats": ["json"],
        },
        {
            "data": [
                {
                    "key": "json",
                    "name": "JSON",
                    "content": (
                        "{\n"
                        "    \"foo\": \"bar\"\n"
                        "}\n"
                    ),
                },
            ],
        }
    ),
])
def test_post_success(client, data, expected_palette):
    """
    On success, palette post view should return JSON with named colors
    """
    url = reverse('django_palette:dump-post')

    response = client.post(
        url,
        json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == 200

    content_json = json.loads(response.content.decode('utf-8'))

    assert content_json == expected_palette
