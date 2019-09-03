from visitorapp.api_request import (
    create_trader, get_prices, open_sell_order, open_buy_order,
    check_order, check_bank)
from visitorapp.db_request import (
    check_bot, get_quantity_bnb, get_markets, save_order, update_order,
    save_trade, update_trade, get_last_trade, save_bank, get_currencies,
    save_error, get_offset, update_offset)
from math import floor, ceil


def check_trade_completed(trader, trade, wait_trade_completed, offset):
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
            # save the new bank and get fee for the trade
            fee = save_bank(new_bank, offset)
            # update trade as completed and new offset
            update_trade(trade, fee)
            wait_trade_completed = False
    else:
        trade_orders = [trade.order_one, trade.order_two, trade.order_three]
        for trade_order in trade_orders:
            if not trade_order.is_completed:
                # request api to know if order is completed now
                order = check_order(
                    trader, trade_order.market.symbol)
                if isinstance(order, str):
                    save_error(order)
                elif order == []:
                    # update order
                    update_order(trade_order.id)
    return wait_trade_completed


def trading():
    trader = create_trader()
    # check if the last trade is completed
    last_trade = get_last_trade()
    offset = get_offset()
    q_bnb = get_quantity_bnb()
    if last_trade is not None:
        if not last_trade.is_completed:
            wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                last_trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, last_trade,
                    wait_trade_completed, offset.bnb * q_bnb)
                if not wait_trade_completed:
                    # update offset
                    offset = update_offset(offset)
    market_one, market_two, market_three = get_markets()
    # set quantity of bnb to trade, offsets and wait for trade completed
    sell_m_one = q_bnb * (1 - offset.bnb)
    buy_m_two = q_bnb * (1 - (offset.bnb / 2))
    buy_m_one = q_bnb * (1 + offset.bnb)
    sell_m_two = q_bnb * (1 + (offset.bnb / 2))
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
                    sell_m_one,
                    prices[market_one])
                open_buy_order(
                    trader, market_two,
                    floor((buy_m_two * 1000 * prices[market_one]) / prices[market_two]) / 1000,
                    prices[market_two])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Sell",
                    str(sell_m_one),
                    str(prices[market_one]))
                order_two = save_order(
                    market_two, "Buy",
                    str(floor((buy_m_two * 1000 * prices[market_one]) / prices[market_two]) / 1000),
                    str(prices[market_two]))
                order_three = save_order(
                    market_three, "Buy",
                    str(q_bnb),
                    str(prices[market_three]))
                save_trade(order_one, order_two, order_three)
                # update offset and wait
                wait_trade_completed = True
            elif rentability <= 0.9977512:
                # open a trade buy on market 1 and sell on markets 2 and 3
                open_sell_order(
                    trader, market_three,
                    q_bnb,
                    prices[market_three])
                open_buy_order(
                    trader, market_one,
                    buy_m_one,
                    prices[market_one])
                open_sell_order(
                    trader, market_two,
                    ceil((sell_m_two * 1000 * prices[market_one]) / prices[market_two]) / 1000,
                    prices[market_two])
                # save orders and trade in db
                order_one = save_order(
                    market_one, "Buy",
                    str(buy_m_one),
                    str(prices[market_one]))
                order_two = save_order(
                    market_two, "Sell",
                    str(ceil((sell_m_two * 1000 * prices[market_one]) / prices[market_two]) / 1000),
                    str(prices[market_two]))
                order_three = save_order(
                    market_three, "Sell",
                    str(q_bnb),
                    str(prices[market_three]))
                save_trade(order_one, order_two, order_three)
                wait_trade_completed = True
            while (check_bot()) and (wait_trade_completed):
                # wait the opened trade is completed
                trade = get_last_trade()
                wait_trade_completed = check_trade_completed(
                    trader, trade,
                    wait_trade_completed, offset.bnb * q_bnb)
                if not wait_trade_completed:
                    # update offset and wait
                    offset = update_offset(offset)
                    sell_m_one = q_bnb * (1 - offset.bnb)
                    buy_m_two = q_bnb * (1 - (offset.bnb / 2))
                    buy_m_one = q_bnb * (1 + offset.bnb)
                    sell_m_two = q_bnb * (1 + (offset.bnb / 2))
        else:
            # save error in db
            save_error(prices)
