from django.utils import timezone
from time import sleep
from visitorapp.models import Bot, Market, Error
from visitorapp.api_request import (
    check_rentability, open_trade_one, open_trade_two)


MARKETS = Market.objects.all().order_by("position")
MARKET_ONE = MARKETS[0].symbol
MARKET_TWO = MARKETS[1].symbol
MARKET_THREE = MARKETS[2].symbol


def update_offset(btc_eth, bnb):
    """ update the offset to change the currency that loose
    at each trade completed """
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
    return btc_eth, bnb, offset_btc_eth, offset_bnb


def trading():
    # set the offsets for the first trade
    btc_eth = 1
    offset_btc_eth = (0.001, 0)
    offset_bnb = 0.01
    bnb = False
    while Bot.objects.all().first().is_working:
        # get the rentabilty for the trade with present prices
        prices, rentability = check_rentability(
            MARKET_ONE, MARKET_TWO, MARKET_THREE)
        if prices != "Error":
            # check the rentabilty
            if rentability > 1.00245:
                # open a trade sell on market 1 and buy on markets 2 and 3
                open_trade_one()
                # update offset
                btc_eth, bnb, offset_btc_eth, offset_bnb = update_offset(
                    btc_eth, bnb)
            elif rentability < 0.997556:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_trade_two()
                # update offset
                btc_eth, bnb, offset_btc_eth, offset_bnb = update_offset(
                    btc_eth, bnb)
            else:
                print("no rentability")
        else:
            # save error in db
            error = Error.objects.all().first()
            error.date = timezone.now()
            error.type_error = rentability
            error.save()
        sleep(1)
