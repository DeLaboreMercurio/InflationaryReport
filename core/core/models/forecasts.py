from django.db import models

class Forecast(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)

    def __str__(self):
        return f"{self.name} - {self.description}"