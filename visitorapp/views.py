from django.shortcuts import render, HttpResponse
from visitorapp.models import Currency, Bank, Bot


def index(request):
    # index view
    if request.is_ajax():
        # visitor want to see all trades
        all_trades = "first trade...."
        return HttpResponse(all_trades)
    # currencies
    currencies = Currency.objects.all().order_by("position")
    # banks
    start_bank = Bank.objects.get(name="start")
    present_bank = Bank.objects.get(name="now")
    # profits
    profit_one = (
        present_bank.amount_currency_one - start_bank.amount_currency_one)
    profit_two = (
        present_bank.amount_currency_two - start_bank.amount_currency_two)
    profit_three = (
        present_bank.amount_currency_three - start_bank.amount_currency_three)
    profits = [profit_one, profit_two, profit_three]
    for i, profit in enumerate(profits):
        if profit > 0:
            profit = "+%.8f" % (profit)
        elif profit < 0:
            profit = "%.8f" % (profit)
        else:
            profit = "0"
        profits[i] = profit
    # bot
    bot_is_working = Bot.objects.all().first().is_working
    context = {
        "currencies": currencies,
        "start_bank": start_bank,
        "present_bank": present_bank,
        "profits": profits,
        "bot_is_working": bot_is_working}
    return render(request, 'visitorapp/index.html', context)
