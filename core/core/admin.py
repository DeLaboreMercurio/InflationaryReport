from django.contrib import admin

from core.models.forecasts import Forecast
from core.models.transactions import Category, Transaction

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Forecast)
