from django.contrib import admin
from visitorapp.models import BinanceKey, Currency, Bank


@admin.register(BinanceKey)
class BinanceKeyAdmin(admin.ModelAdmin):
    list_display = ('api', 'secret')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'amount_currency_one', 'amount_currency_two',
        'amount_currency_three')
