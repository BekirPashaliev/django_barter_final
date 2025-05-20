import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_signup_page_renders(client):
    resp = client.get(reverse("signup"))
    assert resp.status_code == 200
    assert "<h1" in resp.content.decode()
