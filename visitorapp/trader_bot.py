from visitorapp.api_request import (
    create_trader, get_prices, open_sell_order, open_buy_order,
    check_order, check_bank)
from visitorapp.db_request import (
    check_bot, get_quantity_bnb, get_markets, save_order, update_order,
    save_trade, update_trade, get_last_trade, save_bank, get_currencies,
    save_error, get_offset, update_offset, new_update_offset)
from math import floor, ceil


def check_trade_completed(trader, trade, wait_trade_completed):
    # update trade if all orders are completed
    if (trade.order_one.is_completed) and (
        trade.order_two.is_completed) and (
            trade.order_three.is_completed):
        # request api for account bank and save it in db
        currencies = get_currencies()
        new_bank = check_bank(trader, currencies)
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
                trader, trade.order_one.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                # update order
                update_order(trade.order_one.id)
        if not trade.order_two.is_completed:
            # request api to know if order two are completed now
            order = check_order(
                trader, trade.order_two.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                update_order(trade.order_two.id)
        if not trade.order_three.is_completed:
            # request api to know if order three are completed now
            order = check_order(
                trader, trade.order_three.market.symbol)
            if isinstance(order, str):
                save_error(order)
            elif order == []:
                update_order(trade.order_three.id)
    return wait_trade_completed


def trading():
    trader = create_trader()
    # check if the last trade is completed
    last_trade = get_last_trade()
    if last_trade is not None:
        if not last_trade.is_completed:
            wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                last_trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, last_trade, wait_trade_completed)
    market_one, market_two, market_three = get_markets()
    # set quantity of bnb to trade, offsets and wait for trade completed
    quantity_bnb = get_quantity_bnb()
    offset = get_offset()
    wait_trade_completed = False
    while check_bot():
        # get present prices
        prices = get_prices(trader, [market_one, market_two, market_three])
        if isinstance(prices, dict):
            # check the rentabilty
            price_one = prices[market_one]
            price_two = prices[market_two]
            price_three = prices[market_three]
            rentability = price_one / (price_two * price_three)
            if rentability > 1.00245:
                # open orders sell on market 1 and buy on markets 2 and 3
                open_buy_order(
                    trader, market_three,
                    quantity_bnb + offset.bnb,
                    str(price_three + 0.000004)[:8])
                open_sell_order(
                    trader, market_one,
                    quantity_bnb,
                    str(price_one - 0.0000001)[:9])
                open_buy_order(
                    trader, market_two,
                    str(((quantity_bnb * (price_one - 0.0000001)) / (
                        price_two + 0.000001)) + offset.btc)[:5],
                    str(price_two + 0.000001)[:8])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Sell",
                    str(quantity_bnb),
                    str(price_one - 0.0000001)[:9])
                order_two = save_order(
                    market_two, "Buy",
                    str(((quantity_bnb * (price_one - 0.0000001)) / (
                        price_two + 0.000001)) + offset.btc)[:5],
                    str(price_two + 0.000001)[:8])
                order_three = save_order(
                    market_three, "Buy",
                    str(quantity_bnb + offset.bnb),
                    str(price_three + 0.000004)[:8])
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                offset = update_offset(offset)
                wait_trade_completed = True
            elif rentability < 0.997556:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_sell_order(
                    trader, market_three,
                    quantity_bnb - offset.bnb,
                    str(price_three - 0.000004)[:8])
                open_buy_order(
                    trader, market_one,
                    quantity_bnb,
                    str(price_one + 0.0000001)[:9])
                open_sell_order(
                    trader, market_two,
                    str(((quantity_bnb - offset.bnb) * (
                        price_three - 0.000004)) + offset.eth)[:5],
                    str(price_two - 0.000002)[:8])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Buy",
                    str(quantity_bnb),
                    str(price_one + 0.0000001)[:9])
                order_two = save_order(
                    market_three, "Sell",
                    str(quantity_bnb - offset.bnb),
                    str(price_three - 0.000004)[:8])
                order_three = save_order(
                    market_two, "Sell",
                    str(((quantity_bnb - offset.bnb) * (
                        price_three - 0.000004)) + offset.eth)[:5],
                    str(price_two - 0.000002)[:8])
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                offset = update_offset(offset)
                wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                # wait the opened trade is completed
                trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, trade, wait_trade_completed)
        else:
            # save error in db
            save_error(prices)


def new_trading():
    trader = create_trader()
    # check if the last trade is completed
    last_trade = get_last_trade()
    if last_trade is not None:
        if not last_trade.is_completed:
            wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                last_trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, last_trade, wait_trade_completed)
    market_one, market_two, market_three = get_markets()
    # set quantity of bnb to trade, offsets and wait for trade completed
    offset = get_offset()
    q_bnb = get_quantity_bnb()
    sell_q_bnb = q_bnb * (1 - offset.bnb)
    buy_q_bnb = q_bnb * (1 + offset.bnb)
    wait_trade_completed = False
    while check_bot():
        # get present prices
        prices = get_prices(trader, [market_one, market_two, market_three])
        if isinstance(prices, dict):
            rentability = prices[market_one] / (
                prices[market_two] * prices[market_three])
            if rentability >= 1.0022522:
                # open orders sell on market 1 and buy on markets 2 and 3
                open_buy_order(
                    trader, market_three,
                    q_bnb,
                    prices[market_three])
                open_sell_order(
                    trader, market_one,
                    sell_q_bnb,
                    prices[market_one])
                open_buy_order(
                    trader, market_two,
                    floor((q_bnb * 1000 * prices[market_one]) / prices[market_two]) / 1000,
                    prices[market_two])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Sell",
                    str(sell_q_bnb),
                    str(prices[market_one]))
                order_two = save_order(
                    market_two, "Buy",
                    str(floor((q_bnb * 1000 * prices[market_one]) / prices[market_two]) / 1000),
                    str(prices[market_two]))
                order_three = save_order(
                    market_three, "Buy",
                    str(q_bnb),
                    str(prices[market_three]))
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                offset = new_update_offset(offset)
                sell_q_bnb = q_bnb * (1 - offset.bnb)
                buy_q_bnb = q_bnb * (1 + offset.bnb)
                wait_trade_completed = True
            elif rentability <= 0.9977512:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_sell_order(
                    trader, market_three,
                    q_bnb,
                    prices[market_three])
                open_buy_order(
                    trader, market_one,
                    buy_q_bnb,
                    prices[market_one])
                open_sell_order(
                    trader, market_two,
                    ceil((q_bnb * 1000 * prices[market_one]) / prices[market_two]) / 1000,
                    prices[market_two])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Buy",
                    str(buy_q_bnb),
                    str(prices[market_one]))
                order_two = save_order(
                    market_two, "Sell",
                    str(ceil((q_bnb * 1000 * prices[market_one]) / prices[market_two]) / 1000),
                    str(prices[market_two]))
                order_three = save_order(
                    market_three, "Sell",
                    str(q_bnb),
                    str(prices[market_three]))
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                offset = new_update_offset(offset)
                sell_q_bnb = q_bnb * (1 - offset.bnb)
                buy_q_bnb = q_bnb * (1 + offset.bnb)
                wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                # wait the opened trade is completed
                trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, trade, wait_trade_completed)
        else:
            # save error in db
            save_error(prices)
