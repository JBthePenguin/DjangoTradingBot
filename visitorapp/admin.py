from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django import db
from visitorapp.models import (
    BinanceKey, Currency, Bank, Bot, Market, Order, Trade, Error, Offset)
from visitorapp.trader_bot import trading
from multiprocessing import Process


@admin.register(BinanceKey)
class BinanceKeyAdmin(admin.ModelAdmin):
    list_display = ('api', 'secret')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'position')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'amount_currency_one', 'amount_currency_two',
        'amount_currency_three')


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('is_working', "quantity_bnb", "start_date")
    change_list_template = "visitorapp/bot_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('start_stop_bot/', self.start_stop_bot), ]
        return my_urls + urls

    def start_stop_bot(self, request):
        bot = Bot.objects.all().first()
        if bot.is_working:
            bot.is_working = False
        else:
            bot.is_working = True
        bot.save()
        db.connections.close_all()
        if bot.is_working:
            bot_trader = Process(target=trading)
            bot_trader.start()
            self.message_user(request, "Bot is started")
        else:
            self.message_user(request, "Bot is stopped")
        return HttpResponseRedirect("../")


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("symbol", "position")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "get_market", "side", "quantity", "price", "is_completed")

    def get_market(self, obj):
        return "%s" % (obj.market.symbol)

    get_market.admin_order_field = 'market'
    get_market.short_description = 'Market'


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        "open_date", "closed_date", "get_order_one", "get_order_two",
        "get_order_three", "is_completed", "fee")

    def get_order_one(self, obj):
        return "%s" % (obj.order_one.id)

    def get_order_two(self, obj):
        return "%s" % (obj.order_two.id)

    def get_order_three(self, obj):
        return "%s" % (obj.order_three.id)

    get_order_one.admin_order_field = "order_one"
    get_order_one.short_description = "Order one id"
    get_order_two.admin_order_field = "order_two"
    get_order_two.short_description = "Order two id"
    get_order_three.admin_order_field = "order_three"
    get_order_three.short_description = "Order three id"


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ("date", "type_error")


@admin.register(Offset)
class OffsetAdmin(admin.ModelAdmin):
    list_display = ("trade_number", "bnb")
