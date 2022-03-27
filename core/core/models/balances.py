from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Balance(models.Model):
    total = models.DecimalField(
        _("total"), max_digits=10, decimal_places=2, blank=False, default=0
    )
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="balance",
    )

    def __str__(self):
        return f"{self.user}: {self.total}"

    class Meta:
        verbose_name = _('balance')
        verbose_name_plural = _('balances')
