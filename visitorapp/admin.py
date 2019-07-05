from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from visitorapp.models import BinanceKey, Currency, Bank, Bot
from multiprocessing import Process
from time import sleep


def stop_trading(arg=False):
    return arg


def start_trading():
    while True:
        print("bot is running")
        sleep(1)
        if stop_trading():
            break


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
        my_urls = [path('start_bot/', self.start_stop_bot), ]
        return my_urls + urls

    def start_stop_bot(self, request):
        bot = Bot.objects.all().first()
        if bot.is_working:
            bot.is_working = False
        else:
            bot.is_working = True
        bot.save()
        if bot.is_working:
            bot_trader = Process(target=start_trading)
            bot_trader.start()
        else:
            stop_trader = Process(target=stop_trading(True))
            stop_trader.start()
        return HttpResponseRedirect("../")
