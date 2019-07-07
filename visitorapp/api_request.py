from visitorapp.models import BinanceKey, Currency
from binance.client import Client
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
