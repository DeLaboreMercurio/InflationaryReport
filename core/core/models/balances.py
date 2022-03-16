from django.db import models
from django.conf import settings


class Balance(models.Model):

    total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="balance",
    )
