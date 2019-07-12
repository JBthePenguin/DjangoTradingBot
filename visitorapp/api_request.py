from visitorapp.models import BinanceKey, Currency
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from requests.exceptions import ReadTimeout, ConnectionError

BINANCE_KEYS = BinanceKey.objects.all().first()
API_KEY = BINANCE_KEYS.api
SECRET_KEY = BINANCE_KEYS.secret
TRADER = Client(API_KEY, SECRET_KEY)

CURRENCIES = Currency.objects.all()
CURRENCY_ONE = CURRENCIES[0].symbol
CURRENCY_TWO = CURRENCIES[1].symbol
CURRENCY_THREE = CURRENCIES[2].symbol


def check_rentability(market_one, market_two, market_three):
    """ return the current prices for the 3 markets and profitable calcul """
    try:
        prices = {}
        for ticker in TRADER.get_all_tickers():
            if ticker['symbol'] in [market_one, market_two, market_three]:
                prices[ticker['symbol']] = float(ticker['price'])
    except ReadTimeout:
        prices = "Error"
        rentability = "ReadTimeout during check rentability"
    except ConnectionError:
        prices = "Error"
        rentability = "ConnectionError during check rentability"
    except BinanceAPIException:
        prices = "Error"
        rentability = "BinanceAPIException during check rentability"
    else:
        rentability = prices[market_one] / (
            prices[market_two] * prices[market_three])
    return prices, rentability


def open_trade_one(
        market_one, market_two, market_three, prices, offset_bnb,
        offset_btc_eth):
    """open a trade sell on market 1 and buy on markets 2 and 3"""
    # test order
    TRADER.create_test_order(
        symbol=market_one,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=2,
        price=str(prices[market_one] - 0.0000001)[:9])
    TRADER.create_test_order(
        symbol=market_two,
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=str(((2 * (prices[market_one] - 0.0000001)) / (
            prices[market_two] + 0.000001)) + offset_btc_eth[0])[:5],
        price=str(prices[market_two] + 0.000001)[:8])
    TRADER.create_test_order(
        symbol=market_three,
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=2 + offset_bnb,
        price=str(prices[market_three] + 0.000004)[:8])
    # TRADER.order_limit_sell(
    #     symbol=market_one,
    #     quantity=2,
    #     price=str(prices[market_one] - 0.0000001)[:9])
    # TRADER.order_limit_buy(
    #     symbol=market_two,
    #     quantity=str(((2 * (prices[market_one] - 0.0000001)) / (
    #         prices[market_two] + 0.000001)) + offset_btc_eth[0])[:5],
    #     price=str(prices[market_two] + 0.000001)[:8])
    # TRADER.order_limit_buy(
    #     symbol=market_three,
    #     quantity=2 + offset_bnb,
    #     price=str(prices[market_three] + 0.000004)[:8])


def open_trade_two(
        market_one, market_two, market_three, prices, offset_bnb,
        offset_btc_eth):
    """ open a trade buy on market 1 and sell on markets 2 and 3"""
    # test order
    TRADER.create_test_order(
        symbol=market_one,
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=2,
        price=str(prices[market_one] + 0.0000001)[:9])
    TRADER.create_test_order(
        symbol=market_three,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=2 - offset_bnb,
        price=str(prices[market_three] - 0.000004)[:8])
    TRADER.create_test_order(
        symbol=market_two,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=str(((2 - offset_bnb) * (
            prices[market_three] - 0.000004)) + offset_btc_eth[1])[:5],
        price=str(prices[market_two] - 0.000002)[:8])
    # TRADER.order_limit_buy(
    #     symbol=market_one,
    #     quantity=2,
    #     price=str(prices[market_one] + 0.0000001)[:9])
    # TRADER.order_limit_sell(
    #     symbol=market_three,
    #     quantity=2 - offset_bnb,
    #     price=str(prices[market_three] - 0.000004)[:8])
    # TRADER.order_limit_sell(
    #     symbol=market_two,
    #     quantity=str(((2 - offset_bnb) * (
    #         prices[market_three] - 0.000004)) + offset_btc_eth[1])[:5],
    #     price=str(prices[market_two] - 0.000002)[:8])


def check_order(market):
    try:
        order = TRADER.get_open_orders(symbol=market)
    except ReadTimeout:
        order = "ReadTimeout during check order"
    except ConnectionError:
        order = "ConnectionError during check order"
    except BinanceAPIException:
        order = "BinanceAPIException during check order"
    return order


def check_bank():
    """ found balances available for the client """
    while True:
        try:
            balances = TRADER.get_account()['balances']
            bank = {}
            for currency in balances:
                if currency["asset"] in [
                        CURRENCY_ONE, CURRENCY_TWO, CURRENCY_THREE]:
                    bank[currency["asset"]] = float(currency["free"])
        except ReadTimeout:
            pass
        except BinanceAPIException:
            pass
        else:
            break
    return bank
