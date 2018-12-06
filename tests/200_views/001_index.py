import pytest

from django.urls import reverse


def test_ping_index(client):
    """Index view accept GET request"""
    response = client.get(reverse('django_palette:index'))
    assert response.status_code == 200
