from django.shortcuts import get_object_or_404
from rest_framework_json_api import views

from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(views.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    ordering_fields = ('balance',)
    ordering = ('balance',)
    filterset_fields = {
        'balance': ('exact', 'gt', 'gte', 'lt', 'lte',),
    }


class TransactionViewSet(views.ModelViewSet):
    serializer_class = TransactionSerializer
    ordering_fields = ('amount',)
    ordering = ('amount',)
    filterset_fields = {
        'amount': ('exact', 'gt', 'gte', 'lt', 'lte',),
    }

    def get_queryset(self):
        wallet_id: int = self.kwargs['wallet_id']
        return (
            Transaction.objects
            .filter(wallet_id=wallet_id)
            .select_related('wallet')
        )

    def perform_create(self, serializer: TransactionSerializer):
        wallet = get_object_or_404(Wallet, pk=self.kwargs['wallet_id'])
        serializer.save(wallet=wallet)
