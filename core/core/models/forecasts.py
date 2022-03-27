from django.db import models
from django.utils.translation import gettext_lazy as _


class Forecast(models.Model):
    name = models.CharField(_("name"), max_length=100, blank=False)
    description = models.CharField(
        _("description"), max_length=250, blank=True
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    amount = models.DecimalField(
        _("amount"), max_digits=10, decimal_places=2, blank=False, default=0
    )

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name = _('forecast')
        verbose_name_plural = _('forecasts')
