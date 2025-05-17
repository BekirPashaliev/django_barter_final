import pytest
from django.contrib.auth import get_user_model
from ads.models import Ad

@pytest.mark.django_db
def test_create_ad():
    User = get_user_model()
    user = User.objects.create_user(username='user', password='pass')
    ad = Ad.objects.create(user=user, title='Book', description='Some book', category='Books', condition='new')
    assert ad.id is not None
