from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django import db
from visitorapp.models import BinanceKey, Currency, Bank, Bot
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
    list_display = ('is_working',)
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
            self.message_user(request, "Le bot a démarré")
        else:
            self.message_user(request, "Le Bot est arrêté")
        return HttpResponseRedirect("../")
