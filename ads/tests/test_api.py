import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ads.models import Ad, ExchangeProposal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(api_client):
    User = get_user_model()
    u = User.objects.create_user("apiuser", password="Pass12345")
    api_client.login(username="apiuser", password="Pass12345")
    return u


@pytest.mark.django_db
def test_api_ad_crud(api_client, user):
    # 1) создание
    url = reverse("ad-list")  # DRF router name
    payload = {
        "title": "API Lamp",
        "description": "White lamp",
        "category": "Tech",
        "condition": "new",
    }
    resp = api_client.post(url, payload, format="json")
    assert resp.status_code == 201
    ad_id = resp.data["id"]
    # 2) чтение
    resp = api_client.get(f"{url}{ad_id}/")
    assert resp.data["title"] == "API Lamp"
    # 3) обновление
    resp = api_client.patch(f"{url}{ad_id}/", {"condition": "used"}, format="json")
    assert resp.data["condition"] == "used"
    # 4) удаление
    assert api_client.delete(f"{url}{ad_id}/").status_code == 204


@pytest.mark.django_db
def test_api_exchange_flow(api_client, user):
    # подготовим два объявления от разных юзеров
    other = get_user_model().objects.create_user("bob", password="123123Aa")
    ad_sender = Ad.objects.create(user=user, title="Book", description="A", category="Books", condition="new")
    ad_receiver = Ad.objects.create(user=other, title="Bike", description="B", category="Sport", condition="used")

    prop_url = reverse("exchangeproposal-list")
    resp = api_client.post(
        prop_url,
        {"ad_sender": ad_sender.id, "ad_receiver": ad_receiver.id, "comment": "swap?"},
        format="json",
    )
    assert resp.status_code == 201
    proposal_id = resp.data["id"]

    # юзер-инициатор видит статус pending
    resp = api_client.get(prop_url)
    assert resp.data[0]["status"] == "pending"

    # другой пользователь принимает обмен
    api_client.logout()
    api_client.login(username="bob", password="123123Aa")
    resp = api_client.patch(f"{prop_url}{proposal_id}/", {"status": "accepted"}, format="json")
    assert resp.data["status"] == "accepted"
