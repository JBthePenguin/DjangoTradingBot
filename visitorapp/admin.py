from django.contrib import admin
from visitorapp.models import Binance


@admin.register(Binance)
class BinanceAdmin(admin.ModelAdmin):
    list_display = (
        'api_key', 'secret_key', 'currency_one', 'currency_two',
        'currency_three', 'market_one', 'market_two', 'market_three')
