import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_profile_auto_created(client):
    User = get_user_model()
    u = User.objects.create_user("tester", password="12345678")
    assert hasattr(u, "profile")
