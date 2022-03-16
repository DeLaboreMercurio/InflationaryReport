from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from crum import get_current_user

from core.models.balances import Balance


class TransactionTypes(models.TextChoices):
    INCOMING = "IN", _("Incoming")
    OUTGOING = "OUT", _("Outgoing")
    STARTING = "ST", _("Starting")


class Transaction(models.Model):

    type = models.CharField(max_length=3, choices=TransactionTypes.choices, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100, blank=True)

    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions"
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        _update_user_balance(self, current_user)
        self.creator = current_user
        super(Transaction, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    type = models.CharField(
        max_length=3,
        choices=TransactionTypes.choices,
        blank=False,
        default=TransactionTypes.OUTGOING,
    )

    def __str__(self):
        return self.name


def _update_user_balance(transaction, user):
    balance = Balance.objects.get(user=user)
    if transaction.type == TransactionTypes.INCOMING:
        balance.total += transaction.amount
    elif transaction.type == TransactionTypes.OUTGOING:
        balance.total -= transaction.amount
    else:
        raise ValueError("Invalid transaction type")
    balance.save()
