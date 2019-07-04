from visitorapp.models import Binance
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import ReadTimeout

BINANCE = Binance.objects.all().first()
API_KEY = BINANCE.api_key
SECRET_KEY = BINANCE.secret_key
CURRENCY_ONE = BINANCE.currency_one
CURRENCY_TWO = BINANCE.currency_two
CURRENCY_THREE = BINANCE.currency_three
TRADER = Client(API_KEY, SECRET_KEY)


def check_bank():
    """ found balances available for the client """
    while True:
        try:
            balances = TRADER.get_account()['balances']
        except ReadTimeout:
            print("Error Connect for checking bank")
        except BinanceAPIException:
            print("Error Binance API for bank")
        else:
            break
    return balances
