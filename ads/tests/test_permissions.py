import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad


@pytest.mark.django_db
def test_cannot_edit_foreign_ad(client):
    """Пользователь не должен редактировать чужое объявление."""
    User = get_user_model()
    owner = User.objects.create_user("alice", password="123")
    stranger = User.objects.create_user("bob", password="123")
    ad = Ad.objects.create(user=owner, title="Гитара", description="Yamaha",
                           category="Music", condition="used")

    client.login(username="bob", password="123")
    resp = client.post(
        reverse("ads:ad_edit", args=[ad.id]),
        {"title": "Hack", "description": "Hack", "category": "Hack", "condition": "new"},
    )
    # mixin UserPassesTestMixin даёт ответ 403
    assert resp.status_code == 403


@pytest.mark.django_db
def test_cannot_offer_to_self(client):
    """Нельзя предложить обмен своим же объявлением."""
    User = get_user_model()
    user = User.objects.create_user("carol", password="123")
    ad1 = Ad.objects.create(user=user, title="Книга", description="Dune",
                            category="Books", condition="new")
    ad2 = Ad.objects.create(user=user, title="Флешка", description="16 GB",
                            category="Tech", condition="used")

    client.login(username="carol", password="123")

    resp = client.post(
        reverse("ads:proposal_create"),
        {"ad_sender": ad1.id, "ad_receiver": ad2.id, "comment": "swap"},
    )
    # форма вернёт 200 (invalid) — проверяем текст ошибки
    page = resp.content.decode("utf-8")
    assert resp.status_code == 200
    assert "Нельзя обмениваться двумя своими объявлениями" in page