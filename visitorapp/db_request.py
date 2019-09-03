from django.utils import timezone
from visitorapp.models import (
    Market, Bot, BinanceKey, Order, Trade, Bank, Currency, Error, Offset)


def get_keys():
    """ return binance keys api/secret """
    binance_keys = BinanceKey.objects.all().first()
    return binance_keys.api, binance_keys.secret


def get_markets():
    """ return the symbols of the three markets """
    markets = Market.objects.all().order_by("position")
    return markets[0].symbol, markets[1].symbol, markets[2].symbol


def get_quantity_bnb():
    """ return the quantity of bnb to trade """
    return Bot.objects.all().first().quantity_bnb


def check_bot():
    """ return true/false if bot is working """
    return Bot.objects.all().first().is_working


def save_order(market, side, quantity, price):
    """ return the order after save it in db """
    if quantity[-2:] == ".0":
        quantity = quantity[:-2]
    return Order.objects.create(
        market=Market.objects.get(symbol=market),
        side=side,
        quantity=quantity,
        price=price)


def update_order(order_id):
    # update order as completed
    order = Order.objects.get(id=order_id)
    order.is_completed = True
    order.save()


def save_trade(order_one, order_two, order_three):
    """ save trade in db """
    Trade.objects.create(
        order_one=order_one,
        order_two=order_two,
        order_three=order_three)


def get_last_trade():
    """ return the last trade"""
    return Trade.objects.all().last()


def update_trade(trade, fee):
    # update trade as completed
    trade.is_completed = True
    trade.fee = fee
    trade.closed_date = timezone.now()
    trade.save()


def get_currencies():
    """ return the 3 currencies """
    currencies = Currency.objects.all().order_by("position")
    currency_one = currencies[0].symbol
    currency_two = currencies[1].symbol
    currency_three = currencies[2].symbol
    return [currency_one, currency_two, currency_three]


def save_bank(new_bank, offset):
    """ save bank in db and return fee"""
    currencies = get_currencies()
    bank = Bank.objects.get(name="now")
    # calculations of fee
    old_bnb_balance = bank.amount_currency_three
    fee = old_bnb_balance - new_bank[currencies[2]] + offset
    # save bank and return fee
    bank.amount_currency_one = new_bank[currencies[0]]
    bank.amount_currency_two = new_bank[currencies[1]]
    bank.amount_currency_three = new_bank[currencies[2]]
    bank.save()
    return round(fee, 8)


def save_error(type_error):
    """ save the last error in db """
    error = Error.objects.all().first()
    error.date = timezone.now()
    error.type_error = type_error
    error.save()


def get_offset():
    """ return offset """
    return Offset.objects.all().first()


def update_offset(offset):
    trade_number = offset.trade_number
    trade_number += 1
    offset_bnb = 0
    if trade_number == 23:
        trade_number = 1
    else:
        trade_numbers = [4, 9, 13, 18, 22]
        if trade_number in trade_numbers:
            offset_bnb = 0.01
    offset.trade_number = trade_number
    offset.bnb = offset_bnb
    offset.save()
    return offset
