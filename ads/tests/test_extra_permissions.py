import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
def test_anonymous_cannot_create_ad(client):
    """Гость попадает на логин при попытке создать объявление."""
    resp = client.get(reverse("ads:ad_create"))
    # конечный URL должен содержать ?next=/ads/create/
    assert resp.status_code == 302
    assert reverse("login") in resp.url


@pytest.mark.django_db
def test_only_receiver_can_accept_proposal(client):
    """Только владелец ad_receiver может менять статус предложения."""
    User = get_user_model()
    sender = User.objects.create_user("sender", password="123")
    receiver = User.objects.create_user("receiver", password="123")
    outsider = User.objects.create_user("outsider", password="123")

    ad_s = Ad.objects.create(user=sender, title="Ball", description="A", category="Sport", condition="used")
    ad_r = Ad.objects.create(user=receiver, title="Book", description="B", category="Books", condition="new")
    proposal = ExchangeProposal.objects.create(ad_sender=ad_s, ad_receiver=ad_r, comment="swap?")

    # пытается чужой пользователь
    client.login(username="outsider", password="123")
    resp = client.post(reverse("ads:proposal_update", args=[proposal.id]), {"status": "accepted"})
    assert resp.status_code == 404

    # владелец receiver меняет статус
    client.login(username="receiver", password="123")
    resp = client.post(reverse("ads:proposal_update", args=[proposal.id]), {"status": "accepted"}, follow=True)
    proposal.refresh_from_db()
    assert proposal.status == "accepted"


@pytest.mark.django_db
def test_openapi_schema_available(client):
    """Эндпоинт /api/schema/ отдаёт OpenAPI (JSON)."""
    resp = client.get(reverse("schema"))
    assert resp.status_code == 200
    assert "openapi" in resp["content-type"]
