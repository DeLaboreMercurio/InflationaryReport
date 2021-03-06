from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from crum import get_current_user

from core.models.balances import Balance
from core.models.forecasts import Forecast


class TransactionTypes(models.TextChoices):
    INCOMING = "IN", _("Incoming")
    OUTGOING = "OUT", _("Outgoing")
    STARTING = "ST", _("Starting")


class Transaction(models.Model):
    type = models.CharField(
        _("type"), max_length=3, choices=TransactionTypes.choices, blank=False
    )
    amount = models.DecimalField(
        _("amount"), max_digits=10, decimal_places=2, blank=False, default=0
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    description = models.CharField(_("description"), max_length=100, blank=True)

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
    
    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transaction")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=100, blank=False)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    type = models.CharField(
        _("type"), 
        max_length=3,
        choices=TransactionTypes.choices,
        blank=False,
        default=TransactionTypes.OUTGOING,
    )

    associated_forecast = models.ForeignKey(
        Forecast, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


def _update_user_balance(transaction, user):
    balance = Balance.objects.get(user=user)
    if transaction.type == TransactionTypes.INCOMING:
        balance.total += transaction.amount
    elif transaction.type == TransactionTypes.OUTGOING:
        balance.total -= transaction.amount
    else:
        raise ValueError(_("Invalid transaction type"))
    balance.save()
