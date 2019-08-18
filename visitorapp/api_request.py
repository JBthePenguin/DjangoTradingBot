from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import ReadTimeout, ConnectionError
from visitorapp.db_request import get_keys


def create_trader():
    """ create trader with keys and return it """
    api_key, secret_key = get_keys()
    return Client(api_key, secret_key)


def get_prices(trader, markets):
    """ request api to return the current prices for the 3 markets """
    try:
        prices = {}
        for ticker in trader.get_all_tickers():
            if ticker['symbol'] in markets:
                prices[ticker['symbol']] = float(ticker['price'])
    except ReadTimeout:
        prices = "ReadTimeout during check rentability"
    except ConnectionError:
        prices = "ConnectionError during check rentability"
    except BinanceAPIException:
        prices = "BinanceAPIException during check rentability"
    return prices


def open_sell_order(trader, market, quantity, price):
    """ open a sell order """
    trader.order_limit_sell(
        symbol=market,
        quantity=quantity,
        price=price)


def open_buy_order(trader, market, quantity, price):
    """ open a buy order """
    trader.order_limit_buy(
        symbol=market,
        quantity=quantity,
        price=price)


def check_order(trader, market):
    """ check if there is open order on a specific market and
    return it or [] if not """
    try:
        order = trader.get_open_orders(symbol=market)
    except ReadTimeout:
        order = "ReadTimeout during check order"
    except ConnectionError:
        order = "ConnectionError during check order"
    except BinanceAPIException:
        order = "BinanceAPIException during check order"
    return order


def check_bank(trader, currencies):
    """ found balances available for the client """
    try:
        balances = trader.get_account()['balances']
        bank = {}
        for currency in balances:
            if currency["asset"] in currencies:
                bank[currency["asset"]] = float(currency["free"])
    except ReadTimeout:
        bank = "ReadTimeout during check bank"
    except ConnectionError:
        bank = "ConnectionError during check bank"
    except BinanceAPIException:
        bank = "BinanceAPIException during check bank"
    return bank
