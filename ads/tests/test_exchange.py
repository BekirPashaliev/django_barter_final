import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, ExchangeProposal

@pytest.mark.django_db
def test_exchange_proposal_permissions(client):
    User = get_user_model()
    sender = User.objects.create_user('sender', password='pass')
    receiver = User.objects.create_user('receiver', password='pass')
    ad1 = Ad.objects.create(user=sender, title='Book', description='A', category='Books', condition='new')
    ad2 = Ad.objects.create(user=receiver, title='Lamp', description='B', category='Home', condition='used')

    # Login as sender and create proposal
    client.login(username='sender', password='pass')
    resp = client.post(reverse('ads:proposal_create'), {
        'ad_sender': ad1.id,
        'ad_receiver': ad2.id,
        'comment': 'Swap?'
    })
    assert resp.status_code == 302
    proposal = ExchangeProposal.objects.first()
    assert proposal.status == 'pending'

    # Receiver changes status
    client.logout()
    client.login(username='receiver', password='pass')
    resp = client.post(reverse('ads:proposal_update', args=[proposal.id]), {'status': 'accepted'})
    proposal.refresh_from_db()
    assert proposal.status == 'accepted'
