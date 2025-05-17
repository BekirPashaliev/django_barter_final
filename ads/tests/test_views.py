import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_ad_list(client):
    resp = client.get(reverse('ads:ad_list'))
    assert resp.status_code == 200
