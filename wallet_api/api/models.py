from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction


class Wallet(models.Model):
    # I guess label won't be used for searching, because it is not unique
    # That's why it's not indexed
    label = models.CharField(max_length=120)
    balance = models.DecimalField(
        max_digits=30,
        decimal_places=18,
        default=Decimal('0'),
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte=0),
                name='balance_non_negative',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.label} ({self.balance})'


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    txid = models.CharField(
        max_length=128,
        unique=True
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=18,
    )

    def clean(self) -> None:
        if self.amount == 0:
            raise ValidationError('Amount cannot be zero.')

    def save(self, *args, **kwargs):  # noqa: D401
        """Atomic balance update ensuring never-negative wallets."""
        self.full_clean()

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(pk=self.wallet_id)
            new_balance = wallet.balance + self.amount
            if new_balance < 0:
                raise ValidationError('Operation would overdraw wallet.')

            wallet.balance = new_balance
            wallet.save(update_fields=['balance'])

            super().save(*args, **kwargs)
