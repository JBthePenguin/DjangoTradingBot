from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from visitorapp.models import Currency, Bank, Bot, Trade


def index(request):
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
    start_date = Bot.objects.all().first().start_date
    print(start_date)
    # trades completed
    completed_trades = Trade.objects.all().filter(
        is_completed=True).order_by("closed_date").reverse()
    if completed_trades.count() == 0:
        trades_pag = False
    else:
        # pagination
        paginator = Paginator(completed_trades, 2)
        page = request.GET.get('page')
        try:
            trades_pag = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            trades_pag = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            trades_pag = paginator.page(paginator.num_pages)
    # opened trade
    open_trade = Trade.objects.all().filter(is_completed=False)
    context = {
        "currencies": currencies,
        "start_bank": start_bank,
        "present_bank": present_bank,
        "profits": profits,
        "bot_is_working": bot_is_working,
        "start_date": start_date,
        "completed_trades": completed_trades.count(),
        "trades": trades_pag,
        "paginate": True,
        "open_trade": open_trade}
    return render(request, 'visitorapp/index.html', context)
