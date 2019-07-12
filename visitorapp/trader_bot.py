from django.utils import timezone
from time import sleep
from visitorapp.models import Bot, Market, Error, Order, Trade
from visitorapp.api_request import (
    check_rentability, open_trade_one, open_trade_two, check_order)


MARKETS = Market.objects.all().order_by("position")
MARKET_ONE = MARKETS[0].symbol
MARKET_TWO = MARKETS[1].symbol
MARKET_THREE = MARKETS[2].symbol


def save_trade_one(prices, offset_btc_eth, offset_bnb):
    """save orders and trade for trade one"""
    order_one = Order.objects.create(
        market=MARKETS[0],
        side="Sell",
        quantity="2",
        price=str(prices[MARKET_ONE] - 0.0000001)[:9])
    order_two = Order.objects.create(
        market=MARKETS[1],
        side="Buy",
        quantity=str(((2 * (prices[MARKET_ONE] - 0.0000001)) / (
            prices[MARKET_TWO] + 0.000001)) + offset_btc_eth[0])[:5],
        price=str(prices[MARKET_TWO] + 0.000001)[:8])
    order_three = Order.objects.create(
        market=MARKETS[2],
        side="Buy",
        quantity=str(2 + offset_bnb),
        price=str(prices[MARKET_THREE] + 0.000004)[:8])
    Trade.objects.create(
        order_one=order_one,
        order_two=order_two,
        order_three=order_three)


def save_trade_two(prices, offset_btc_eth, offset_bnb):
    """save orders and trade for trade one"""
    order_one = Order.objects.create(
        market=MARKETS[0],
        side="Buy",
        quantity="2",
        price=str(prices[MARKET_ONE] + 0.0000001)[:9])
    order_two = Order.objects.create(
        market=MARKETS[2],
        side="Sell",
        quantity=str(2 - offset_bnb),
        price=str(prices[MARKET_THREE] - 0.000004)[:8])
    order_three = Order.objects.create(
        market=MARKETS[1],
        side="Sell",
        quantity=str(((2 - offset_bnb) * (
            prices[MARKET_THREE] - 0.000004)) + offset_btc_eth[1])[:5],
        price=str(prices[MARKET_TWO] - 0.000002)[:8])
    Trade.objects.create(
        order_one=order_one,
        order_two=order_two,
        order_three=order_three)


def save_error(type_error):
    error = Error.objects.all().first()
    error.date = timezone.now()
    error.type_error = type_error
    error.save()


def update_offset(btc_eth, bnb):
    """ update the offset to change the currency that loose
    at each trade completed and update wait"""
    btc_eth += 1
    bnb = not bnb
    if btc_eth == 5:
        # change offset for btc and eth every 2 trades
        btc_eth = 1
    # update offset for btc and eth
    if (btc_eth == 1) or (btc_eth == 2):
        offset_btc_eth = (0.001, 0)
    else:
        offset_btc_eth = (0, 0.001)
    # update offset for bnb
    if bnb:
        offset_bnb = 0
    else:
        offset_bnb = 0.01
    return btc_eth, bnb, offset_btc_eth, offset_bnb, True


def trading():
    # set the offsets for the first trade
    btc_eth = 1
    offset_btc_eth = (0.001, 0)
    offset_bnb = 0.01
    bnb = False
    wait = False
    while Bot.objects.all().first().is_working:
        # get the rentabilty for the trade with present prices
        prices, rentability = check_rentability(
            MARKET_ONE, MARKET_TWO, MARKET_THREE)
        if prices != "Error":
            # check the rentabilty
            if rentability > 1.00245:
                # open a trade sell on market 1 and buy on markets 2 and 3
                open_trade_one(
                    MARKET_ONE, MARKET_TWO, MARKET_THREE, prices, offset_bnb,
                    offset_btc_eth)
                print("open order one")
                # save orders and trade in db
                save_trade_one(prices, offset_btc_eth, offset_bnb)
                # update offset and wait
                btc_eth, bnb, offset_btc_eth, offset_bnb, wait = update_offset(
                    btc_eth, bnb)
            elif rentability < 0.997556:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_trade_two(
                    MARKET_ONE, MARKET_TWO, MARKET_THREE, prices, offset_bnb,
                    offset_btc_eth)
                print("open order two")
                # save orders and trade in db
                save_trade_two(prices, offset_btc_eth, offset_bnb)
                # update offset
                btc_eth, bnb, offset_btc_eth, offset_bnb, wait = update_offset(
                    btc_eth, bnb)
            else:
                print("no rentability")
            while (Bot.objects.all().first().is_working) and (wait):
                # wait the opened trade is completed
                open_trade = Trade.objects.all().last()
                if (open_trade.order_one.is_completed) and (
                    open_trade.order_two.is_completed) and (
                        open_trade.order_three.is_completed):
                    # update trade as completed
                    open_trade.is_completed = True
                    open_trade.closed_date = timezone.now()
                    open_trade.save()
                    wait = False
                    print("trade completed")
                else:
                    if not open_trade.order_one.is_completed:
                        # request api to know if order one are completed now
                        order = check_order(open_trade.order_one.market.symbol)
                        if isinstance(order, str):
                            save_error(order)
                        elif order == []:
                            order_one = Order.objects.get(
                                id=open_trade.order_one.id)
                            order_one.is_completed = True
                            order_one.save()
                    if not open_trade.order_two.is_completed:
                        # request api to know if order two are completed now
                        order = check_order(open_trade.order_two.market.symbol)
                        if isinstance(order, str):
                            save_error(order)
                        elif order == []:
                            order_two = Order.objects.get(
                                id=open_trade.order_two.id)
                            order_two.is_completed = True
                            order_two.save()
                    if not open_trade.order_three.is_completed:
                        # request api to know if order three are completed now
                        order = check_order(
                            open_trade.order_three.market.symbol)
                        if isinstance(order, str):
                            save_error(order)
                        elif order == []:
                            order_three = Order.objects.get(
                                id=open_trade.order_three.id)
                            order_three.is_completed = True
                            order_three.save()
                    print("wait for last trade completed")
        else:
            # save error in db
            save_error(rentability)
