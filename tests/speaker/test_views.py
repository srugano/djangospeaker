import pytest
import test_helpers

from django.urls import reverse


pytestmark = [pytest.mark.django_db]


def tests_individual_list_view(client):
    instance1 = test_helpers.create_speaker_individual()
    instance2 = test_helpers.create_speaker_individual()
    url = reverse("speaker_individual_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_individual_create_view(client):
    url = reverse("speaker_individual_create")
    data = {
        "voice_sample": "aFile",
        "full_name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_individual_detail_view(client):
    instance = test_helpers.create_speaker_individual()
    url = reverse(
        "speaker_individual_detail",
        args=[
            instance.pk,
        ],
    )
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_individual_update_view(client):
    instance = test_helpers.create_speaker_individual()
    url = reverse(
        "speaker_individual_update",
        args=[
            instance.pk,
        ],
    )
    data = {
        "voice_sample": "aFile",
        "full_name": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302
