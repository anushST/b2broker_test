from decimal import Decimal

import pytest
from api.models import Transaction, Wallet
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def wallet():
    return Wallet.objects.create(label='Owner')


@pytest.mark.django_db
class TestTransactionAPI:

    def _payload(self, wallet_id, txid='t1', amount='5.0'):
        return {
            "data": {
                "type": "Transactions",
                "attributes": {"txid": txid, "amount": amount},
                "relationships": {
                    "wallet": {"data": {"type": "Wallets", "id": str(wallet_id)}}
                },
            }
        }

    def test_create_transaction_updates_balance(self, api_client, wallet):
        url = reverse('transactions', args=[wallet.id])
        r = api_client.post(
            url, self._payload(wallet.id),
        )
        assert r.status_code == status.HTTP_201_CREATED
        wallet.refresh_from_db()
        assert wallet.balance == Decimal("5.0")

    def test_retrieve_transaction(self, api_client, wallet):
        tx = Transaction.objects.create(wallet=wallet, txid="abc", amount="3")
        url = reverse('transaction-detail', args=[wallet.id, tx.id])
        r = api_client.get(url)
        assert r.status_code == status.HTTP_200_OK
        assert r.json()['data']['attributes']['txid'] == 'abc'

    def test_list_transactions(self, api_client, wallet):
        url = reverse('transactions', args=[wallet.id])
        Transaction.objects.create(wallet=wallet, txid='a', amount='1')
        Transaction.objects.create(wallet=wallet, txid='b', amount='2')
        r = api_client.get(url)
        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()["data"]) == 2

    def test_amount_zero_invalid(self, api_client, wallet):
        r = api_client.post(
            reverse('transactions', args=[wallet.id]),
            self._payload(wallet.id, txid='z', amount='0'),
        )
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        data = r.json()
        assert 'amount' in data['errors'][0]['detail'] or data['errors']

    def test_overdraw_blocked(self, api_client, wallet):
        Transaction.objects.create(wallet=wallet, txid='in', amount='3')
        r = api_client.post(
            reverse('transactions', args=[wallet.id]),
            self._payload(wallet.id, txid='out', amount='-10')
        )
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    # Additional we can add tests for pagination, filtering and sorting.
