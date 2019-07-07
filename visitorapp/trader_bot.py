from time import sleep
from visitorapp.models import Bot, Market, Error
from visitorapp.api_request import check_rentability


MARKETS = Market.objects.all().order_by("position")
MARKET_ONE = MARKETS[0].symbol
MARKET_TWO = MARKETS[1].symbol
MARKET_THREE = MARKETS[2].symbol


def trading():
    while Bot.objects.all().first().is_working:
        # check the rentabilty for the trade with present prices
        while Bot.objects.all().first().is_working:
            prices, rentability = check_rentability(
                MARKET_ONE, MARKET_TWO, MARKET_THREE)
            if prices != "Error":
                break
            else:
                error = Error.objects.all().first()
                error.type_error = rentability
                error.save()
        print(prices)
        print(rentability)
        sleep(1)
