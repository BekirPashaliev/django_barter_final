import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_signup_auto_login(client):
    """После регистрации пользователь автоматически залогинен и попадает на /accounts/profile/."""
    resp = client.post(
        reverse("signup"),
        {"username": "newbie", "password1": "StrongPass123!", "password2": "StrongPass123!"},
        follow=True,
    )
    assert resp.status_code == 200
    # Проверяем, что шаблон профиля отрисовался и user.authenticated = True
    assert resp.wsgi_request.user.is_authenticated
    assert "Профиль" in resp.content.decode()


@pytest.mark.django_db
def test_profile_edit(client, django_image_file):
    """Обновление аватара и био."""
    client.post(
        reverse("signup"),
        {"username": "avatar", "password1": "Pass123qwe!", "password2": "Pass123qwe!"},
        follow=True,
    )
    resp = client.post(
        reverse("profile_edit"),
        {"bio": "Hello!", "avatar": django_image_file("pic.jpg", size=(50, 50))},
        follow=True,
    )
    page = resp.content.decode()
    assert "Hello!" in page
