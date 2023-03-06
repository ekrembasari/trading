from trading_ig import IGService
from trading_ig.config import config
from datetime import datetime
import pandas as pd
import time

import requests

ig_service = IGService(config.username, config.password, config.api_key, config.acc_type)

# switch account to the spread betting if its not in default and set it as default
accountId = config.acc_number
try:
    ig_service.switch_account(accountId, True)
    print("Successfully switched the default account to {}".format(accountId))
except:
    print("Your account {} has been already set as default".format(accountId))

while True:
    try:
        ig_service.create_session()
        print("Session created!")
        break
    except Exception as e:
        print(e)
        time.sleep(1)
        continue

epic = config.EPIC_ID
resolution = config.TIME_FRAME
risk = config.RISK_PERC
equity_max_perc = config.EQUITY_MAX_PERCENT
ema_fast = config.EMA_FAST
ema_slow = config.EMA_SLOW
donchian_period = config.DONCHIAN_PERIOD
wait_candles_num = config.WAIT_CANDLES_NUM


def switch_account():
    try:
        res = ig_service.switch_account(accountId, True)
        print("Successfully switched the default account to {}".format(accountId))
    except:
        print("Your account {} has been already set as default".format(accountId))


def get_donchian():
    try:
        response = ig_service.fetch_historical_prices_by_epic_and_num_points(epic, resolution, donchian_period+5)
    except Exception as e:
        print(e)
        return 0, 0

    df_ask = response['prices']['ask']
    df_ask = df_ask.reset_index(col_level=0)

    df_bid = response['prices']['bid']
    df_bid = df_bid.reset_index(col_level=0)

    buy_stop_loss = min((df_ask['Low']/2+df_bid['Low']/2).tolist()[-donchian_period:])
    sell_stop_loss = max((df_ask['High']/2+df_bid['High']/2).tolist()[-donchian_period:])

    return buy_stop_loss, sell_stop_loss


def buy_sell_trigger():

    buy_trigger = False
    sell_trigger = False

    try:
        f = open('last_id', 'r')
        last_id = int(f.readlines()[0][:-1])
        f.close()
    except:
        last_id = 0
    
    try:
        url = 'https://collect2.com/api/46fb7ae8-2126-49c1-ad73-6ce4ea2f69df/datarecord/'
        res = requests.get(url).json()
    except Exception as e:
        print(e)
        return False, False

    if res["count"] == 0:
        return False, False

    if res["results"][0]["id"] == last_id:
        return False, False
    else:
        last_id = res["results"][0]["id"]
        f = open('last_id', 'w')
        f.write(str(last_id)+'\n')
        f.close()

        trigger = res["results"][0]["record"]["type"]
        if trigger == "long":
            buy_trigger = True
        if trigger == "short":
            sell_trigger = True

        return buy_trigger, sell_trigger



def get_size(action, order_price, stop_loss):
    try:
        account_info = ig_service.fetch_accounts()
    except Exception as e:
        print(e)
        return 0

    print(account_info)
    balance = account_info[account_info['accountId']==accountId].reset_index(drop=True).iloc[0]['available']
    print(balance)

    equity_max = (((balance * 20) / order_price) * (100 - equity_max_perc) / 100) // 0.01 / 100
    if action == 'BUY':
        stop_loss_max = abs(((balance * risk/100) / (order_price - stop_loss)) // 0.01 / 100)
    else:
        stop_loss_max = abs(((balance * risk/100) / (stop_loss - order_price)) // 0.01 / 100)
    
    print(equity_max, stop_loss_max)

    size = min(equity_max, stop_loss_max)
    return size


def close_positions(action):
    try:
        current_positions = ig_service.fetch_open_positions()
    except Exception as e:
        print(e)
        return False

    if current_positions.shape[0] < 1:
        print("No open positions to close...")
        return True

    current_position = current_positions.iloc[0]
    deal_id = current_position['position']['dealId']
    size = current_position['position']['dealSize']
    direction = current_position['position']['direction']
    expiry = current_position['market']['expiry']
    epic = current_position['market']['epic']
    
    if action != direction:
        try:
            res = ig_service.close_open_position(deal_id, action, None, None, None, 'MARKET', None, size)
        except Exception as e:
            print(e)
            return False

        if res['reason'] == "SUCCESS":
            print('Position closed successfully!')
            return True
        else:
            print('Position not closed due to {} reason.'.format(res['reason']))
            return False

    print("Previous position is in the same direction.")
    return False


def place_order(action, stop_loss):
    order_flag = close_positions(action)
    if not order_flag:
        print("Skip trade...")
        return None
    
    try:
        current_market = ig_service.fetch_market_by_epic(epic)['snapshot']
    except Exception as e:
        print(e)
        return None

    print(current_market)
    if action == 'BUY':
        order_price = current_market['offer']
    else:
        order_price = current_market['bid']

    size = get_size(action, order_price, stop_loss)
    print(order_price, size)
    if size < 1:
        return None

    try:
        res_create = ig_service.create_open_position(
            currency_code='GBP',
            direction=action,
            epic=epic,
            expiry='DFB',
            force_open=True,
            guaranteed_stop=False,
            level=None,
            order_type='MARKET',
            size=size,
            stop_distance=None,
            limit_distance=None,
            limit_level=None,
            quote_id=None,
            stop_level=stop_loss,
            trailing_stop=None,
            trailing_stop_increment=None)
    except Exception as e:
        print(e)
        return None

    if res_create['reason'] == 'SUCCESS':
        print("Order placed successfully! Here is your order detail.")
        print(res_create)
    else:
        print("Order not placed due to {}.".format(res_create['reason']))
        print(res_create)
        return res_create

    return res_create


def trade():

    while True:

        print(f"\n\nCurrent time: {datetime.now()}\n")

        print("Start checking if any buy/sell condition meets now...")

        try:
            print(ig_service.fetch_market_by_epic(config.EPIC_ID))
        except Exception as e:
            print(e)
            time.sleep(1)
            continue

        buy_trigger, sell_trigger = buy_sell_trigger()

        if buy_trigger:
            print("Buying is triggered now.")
            buy_stop_loss, sell_stop_loss = get_donchian()
            if buy_stop_loss == 0:
                continue
            print("Stop loss: ", buy_stop_loss)
            place_order("BUY", buy_stop_loss)
        else:
            print("Buying is not triggered.")
        if sell_trigger:
            print("Selling is triggered now.")
            buy_stop_loss, sell_stop_loss = get_donchian()
            if sell_stop_loss == 0:
                continue
            print("Stop loss: ", sell_stop_loss)
            place_order("SELL", sell_stop_loss)
        else:
            print("Selling is not triggered now.")

        print("\nLooping...\n")
        time.sleep(2)


if __name__=="__main__":
    trade()
