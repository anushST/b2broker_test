# tests/test_wallet.py
from decimal import Decimal

import pytest
from api.models import Wallet
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestWalletAPI:
    """CRUD over /api/wallets/"""

    list_url = reverse('wallet-list')

    def test_create_wallet(self, api_client):
        payload = {
            'data': {
                'type': 'Wallets',
                'attributes': {'label': 'My Wallet'}
            }
        }
        r = api_client.post(self.list_url, payload)
        assert r.status_code == status.HTTP_201_CREATED
        data = r.json()['data']['attributes']
        assert data['label'] == 'My Wallet'
        assert Decimal(data['balance']) == Decimal("0")
        assert Wallet.objects.filter(label='My Wallet').count() == 1

    def test_retrieve_wallet(self, api_client):
        wallet = Wallet.objects.create(label="Show")
        url = reverse("wallet-detail", args=[wallet.id])
        r = api_client.get(url)
        assert r.status_code == status.HTTP_200_OK
        assert r.json()["data"]["attributes"]["label"] == "Show"

    def test_list_wallets(self, api_client):
        Wallet.objects.bulk_create(
            [Wallet(label="A"), Wallet(label="B")]
        )
        r = api_client.get(self.list_url)
        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()["data"]) == 2

    def test_update_wallet(self, api_client):
        wallet = Wallet.objects.create(label="Old")
        url = reverse("wallet-detail", args=[wallet.id])
        patch = {
            "data": {
                "type": "Wallets",
                "id": str(wallet.id),
                "attributes": {"label": "New Name"}
            }
        }
        r = api_client.patch(url, patch)
        assert r.status_code == status.HTTP_200_OK
        wallet.refresh_from_db()
        assert wallet.label == "New Name"

    def test_delete_wallet(self, api_client):
        wallet = Wallet.objects.create(label="Tmp")
        url = reverse("wallet-detail", args=[wallet.id])
        r = api_client.delete(url)
        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert not Wallet.objects.filter(pk=wallet.id).exists()

    # Additional we can add tests for pagination, filtering and sorting.


@pytest.mark.django_db
def test_wallet_balance_cannot_be_negative():
    wallet = Wallet.objects.create(label="Safe")
    wallet.balance = Decimal("-1")
    with pytest.raises(IntegrityError):
        wallet.save(force_update=True)
