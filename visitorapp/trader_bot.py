from time import sleep
from visitorapp.api_request import (
    create_trader, get_prices, open_sell_order, open_buy_order,
    check_order, check_bank)
from visitorapp.db_request import (
    check_bot, get_markets, save_order, update_order, save_trade,
    update_trade, get_last_trade, save_bank, get_currencies, save_error)


TRADER = create_trader()


def check_trade_completed(trade, wait_trade_completed):
    # update trade if all orders are completed
    if (trade.order_one.is_completed) and (
        trade.order_two.is_completed) and (
            trade.order_three.is_completed):
        # request api for account bank and save it in db
        currencies = get_currencies()
        new_bank = check_bank(TRADER, currencies)
        if isinstance(new_bank, str):
            save_error(new_bank)
        else:
            save_bank(new_bank)
            # update trade as completed
            update_trade(trade)
            wait_trade_completed = False
    else:
        if not trade.order_one.is_completed:
            # request api to know if order one are completed now
            order = check_order(
                TRADER, trade.order_one.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                # update order
                update_order(trade.order_one.id)
        if not trade.order_two.is_completed:
            # request api to know if order two are completed now
            order = check_order(
                TRADER, trade.order_two.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                update_order(trade.order_two.id)
        if not trade.order_three.is_completed:
            # request api to know if order three are completed now
            order = check_order(
                TRADER, trade.order_three.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                update_order(trade.order_three.id)
    return wait_trade_completed


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
    return btc_eth, bnb, offset_btc_eth, offset_bnb


def trading():
    # check if the last trade is completed
    last_trade = get_last_trade()
    if last_trade is not None:
        if not last_trade.is_completed:
            wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                wait_trade_completed = check_trade_completed(
                    last_trade, wait_trade_completed)
    market_one, market_two, market_three = get_markets()
    # set the offsets for the first trade
    btc_eth = 1
    offset_btc_eth = (0.001, 0)
    offset_bnb = 0.01
    bnb = False
    # set wait for trade completed
    wait_trade_completed = False
    while check_bot():
        # get present prices
        prices = get_prices(TRADER, [market_one, market_two, market_three])
        if isinstance(prices, dict):
            # check the rentabilty
            price_one = prices[market_one]
            price_two = prices[market_two]
            price_three = prices[market_three]
            rentability = price_one / (price_two * price_three)
            print(rentability)
            if rentability > 1.00245:
                # open orders sell on market 1 and buy on markets 2 and 3
                open_sell_order(
                    TRADER, market_one,
                    2,
                    str(price_one - 0.0000001)[:9])
                open_buy_order(
                    TRADER, market_two,
                    str(((2 * (price_one - 0.0000001)) / (
                        price_two + 0.000001)) + offset_btc_eth[0])[:5],
                    str(price_two + 0.000001)[:8])
                open_buy_order(
                    TRADER, market_three,
                    2 + offset_bnb,
                    str(price_three + 0.000004)[:8])
                print("open order one")
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Sell",
                    "2",
                    str(price_one - 0.0000001)[:9])
                order_two = save_order(
                    market_two, "Buy",
                    str(((2 * (price_one - 0.0000001)) / (
                        price_two + 0.000001)) + offset_btc_eth[0])[:5],
                    str(price_two + 0.000001)[:8])
                order_three = save_order(
                    market_three, "Buy",
                    str(2 + offset_bnb),
                    str(price_three + 0.000004)[:8])
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                btc_eth, bnb, offset_btc_eth, offset_bnb = update_offset(
                    btc_eth, bnb)
                wait_trade_completed = True
            elif rentability < 0.997556:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_buy_order(
                    TRADER, market_one,
                    2,
                    str(price_one + 0.0000001)[:9])
                open_sell_order(
                    TRADER, market_three,
                    2 - offset_bnb,
                    str(price_three - 0.000004)[:8])
                open_sell_order(
                    TRADER, market_two,
                    str(((2 - offset_bnb) * (
                        price_three - 0.000004)) + offset_btc_eth[1])[:5],
                    str(price_two - 0.000002)[:8])
                print("open order two")
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Buy",
                    "2",
                    str(price_one + 0.0000001)[:9])
                order_two = save_order(
                    market_three, "Sell",
                    str(2 - offset_bnb),
                    str(price_three - 0.000004)[:8])
                order_three = save_order(
                    market_two, "Sell",
                    str(((2 - offset_bnb) * (
                        price_three - 0.000004)) + offset_btc_eth[1])[:5],
                    str(price_two - 0.000002)[:8])
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                btc_eth, bnb, offset_btc_eth, offset_bnb = update_offset(
                    btc_eth, bnb)
                wait_trade_completed = True
            else:
                print("no rentability")
            while (check_bot()) and (wait_trade_completed):
                # wait the opened trade is completed
                trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trade, wait_trade_completed)
        else:
            # save error in db
            save_error(prices)
