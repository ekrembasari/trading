import os


class config(object):
    username = os.environ.get("IG_USERNAME", "")
    password = os.environ.get("IG_PASSWORD", "")
    api_key = os.environ.get("IG_API_KEY", "")
    acc_type = os.environ.get("IG_ACC_TYPE", "DEMO")
    acc_number = os.environ.get("IG_ACC_NUMBER", "")

    # define parameters for the strategy
    EPIC_ID = "IX.D.FTSE.DAILY.IP" # This one is IG compatible id of FTSE100
    TIME_FRAME = "10MIN"  # 'S', 'MIN', '2MIN', '3MIN', '5MIN', '10MIN', '15MIN', '30MIN',
                        # 'H', '2H', '3H', '4H', 'D', 'W', 'M'
    WAIT_CANDLES_NUM = 1

    RISK_PERC = 5 # Percent(%)
    EQUITY_MAX_PERCENT = 10 # Percent(%)
    EMA_FAST = 2
    EMA_SLOW = 5
    DONCHIAN_PERIOD = 10

    SYMBOL = 'FTSE'
    API_12DATA = 'N/A'
