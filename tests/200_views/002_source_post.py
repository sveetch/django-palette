import json

import pytest

from django.urls import reverse


def test_get_notallowed(client):
    """
    Source post view should return an http405 since it does not accept GET
    """
    url = reverse("django_palette:source-post")
    response = client.get(url)
    assert response.status_code == 405


@pytest.mark.parametrize("data,expected", [
    (
        {
            "foo": "bar",
        },
        {
            "source": [
                "This field is required."
            ],
        },
    ),
    (
        {
            "source": "nope",
        },
        {
            "source": [
                "Source does not contain any valid color value"
            ],
        },
    ),
])
def test_post_error(client, data, expected):
    """
    On error, source post view should return a http400 with correct message
    in JSON
    """
    url = reverse("django_palette:source-post")

    response = client.post(
        url,
        json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == 400

    content_json = json.loads(response.content.decode("utf-8"))

    assert content_json.get("data") == expected


@pytest.mark.parametrize("data,expected", [
    (
        {"source": "#F0F0F0\n#FF0000\n#F0F0F0\n#FF0000\n#000000"},
        {
            "#f0f0f0": [
                ["grey94", "#f0f0f0"],
                ['white', '#ffffff']
            ],
            "#ff0000": [
                ['red1', '#ff0000'],
                ['scarlet', '#fc2847']
            ],
            "#000000": [
                ['black', '#000000'],
                ['black', '#000000']
            ]
        },
    ),
])
def test_post_success(testsettings, settings, client, data, expected):
    """
    On success, source post view should return JSON with computed named colors
    """
    # Mock available registries for a lighter list
    settings.PALETTE_AVAILABLE_REGISTRIES = testsettings.available_registries

    url = reverse("django_palette:source-post")

    response = client.post(
        url,
        json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == 200

    content_json = json.loads(response.content.decode("utf-8"))

    assert content_json.get("data") == expected
