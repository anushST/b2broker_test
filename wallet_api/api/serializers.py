from decimal import Decimal

from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'label', 'balance',)
        read_only_fields = ('balance',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'wallet', 'txid', 'amount')

    def validate_amount(self, value: Decimal) -> Decimal:
        if value == 0:
            raise ValidationError('Amount cannot be zero.')
        return value

    def validate(self, attrs):
        """
        It is pre check. Final check is in Transaction.save
        """
        wallet: Wallet | None = attrs.get('wallet') or getattr(self.instance, 'wallet', None)
        amount: Decimal | None = attrs.get('amount')

        if wallet is not None and amount is not None:
            projected_balance = wallet.balance + amount
            if projected_balance < 0:
                raise ValidationError(
                    {'amount': 'Operation would overdraw wallet.'}
                )
        return attrs
