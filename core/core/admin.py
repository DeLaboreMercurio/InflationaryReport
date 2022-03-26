from django.contrib import admin
from core.models.forecasts import *
from core.models.transactions import *

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Forecast)
