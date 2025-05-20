import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad


@pytest.mark.django_db
def test_search_and_filter(client):
    User = get_user_model()
    u = User.objects.create_user("searcher", password="123")
    Ad.objects.create(user=u, title="iPhone 11", description="смартфон", category="Tech", condition="used")
    Ad.objects.create(user=u, title="iPhone 14 Pro", description="новый", category="Tech", condition="new")
    Ad.objects.create(user=u, title="Настольная игра", description="Каркассон", category="Games", condition="used")

    # поиск по ключевому слову
    resp = client.get(reverse("ads:ad_list"), {"q": "iphone"})
    assert resp.status_code == 200
    assert "iPhone 11" in resp.content.decode()
    assert "Настольная игра" not in resp.content.decode()

    # фильтр по категории и состоянию
    resp = client.get(reverse("ads:ad_list"), {"category": "Tech", "condition": "new"})
    page = resp.content.decode()
    assert "iPhone 14 Pro" in page
    assert "iPhone 11" not in page
