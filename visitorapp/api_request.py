from visitorapp.models import BinanceKey, Currency
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import ReadTimeout

BINANCE_KEYS = BinanceKey.objects.all().first()
API_KEY = BINANCE_KEYS.api
SECRET_KEY = BINANCE_KEYS.secret
TRADER = Client(API_KEY, SECRET_KEY)

CURRENCIES = Currency.objects.all()
CURRENCY_ONE = CURRENCIES[0].symbol
CURRENCY_TWO = CURRENCIES[1].symbol
CURRENCY_THREE = CURRENCIES[2].symbol


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
