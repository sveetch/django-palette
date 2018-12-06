import json

import pytest

from django.urls import reverse


def test_get_notallowed(client):
    """
    Source post view should return an http405 since it does not accept GET
    """
    url = reverse('django_palette:palette-post')
    response = client.get(url)
    assert response.status_code == 405


@pytest.mark.parametrize("data,expected", [
    # second form fields are empty
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "dummy",
            "form-0-name": "fake",
            "form-1-color": "",
            "form-1-name": "",
        },
        [
            {},
            {
                'name': ['This field is required.'],
                'color': ['This field is required.'],
            }
        ],
    ),
    # Ensure malformed POST request for formset does not trigger http500
    (
        {
            'wrong': 'nope',
        },
        [
            {
                'global': ['Malformed formset POST request']
            }
        ],
    ),
])
def test_post_error(client, data, expected):
    """
    On error, palette post view should return a http400 with correct message
    in JSON
    """
    url = reverse('django_palette:palette-post')

    response = client.post(
        url,
        data
    )

    assert response.status_code == 400

    content_json = json.loads(response.content.decode('utf-8'))

    assert content_json.get('data') == expected


@pytest.mark.parametrize("data,expected", [
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "dummy",
            "form-0-name": "fake",
            "form-1-color": "foo",
            "form-1-name": "bar",
        },
        [
            {'color': 'dummy', 'name': 'fake'},
            {'color': 'foo', 'name': 'bar'}
        ],
    ),
])
def test_post_success(client, data, expected):
    """
    On success, palette post view should return JSON with named colors
    """
    url = reverse('django_palette:palette-post')

    response = client.post(
        url,
        data
    )

    assert response.status_code == 200

    content_json = json.loads(response.content.decode('utf-8'))

    assert content_json.get('data') == expected
