# coding=utf-8

import ccxt

#print(ccxt.exchanges[1])  Exchanges array
'''
hitbtc   = ccxt.hitbtc({'verbose': True})
bitmex   = ccxt.bitmex()
huobipro = ccxt.huobipro()
exmo     = ccxt.exmo({
    'apiKey': 'YOUR_PUBLIC_API_KEY',
    'secret': 'YOUR_SECRET_PRIVATE_KEY',
})
kraken = ccxt.kraken({
    'apiKey': 'YOUR_PUBLIC_API_KEY',
    'secret': 'YOUR_SECRET_PRIVATE_KEY',
})
'''
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)

exchange = exchange_class({
    'apiKey': 'XTZrjPgM6xBoUXqINR68nOz7Fog7b9aMkIuwYzHxtvxZ1uniwmUYwLlyUHeQeVIk',
    'secret': 'UBELB7W8XcL5gjihNhzhZXPf9Zu63HRYzAwuaUrfNV3Ry6SQM8upfbNnWKgFydkW',
    'timeout': 30000,
    'enableRateLimit': True,
})


#print(exchange.fetch_balance())
#print(exchange.id, exchange.load_markets()["ETH/USDT"]["info"])

#print(exchange.fetch_order_book(symbol='BTC/USDT'))

symbol = 'BTC/USDT'  
type = 'limit'  # or 'market'
side = 'sell'  # or 'buy'
amount = 1.0
price = 50000  # or None

# extra params and overrides if needed
params = {
    'test': True,  # test if it's valid, but don't actually place it
}

order = exchange.create_order(symbol, type, side, amount, price, params)

print(order)
'''
hitbtc_markets = hitbtc.load_markets()

print(hitbtc.id, hitbtc_markets)
print(bitmex.id, bitmex.load_markets())
print(huobipro.id, huobipro.load_markets())

print(hitbtc.fetch_order_book(hitbtc.symbols[0]))
print(bitmex.fetch_ticker('BTC/USD'))
print(huobipro.fetch_trades('LTC/USDT'))

print(exmo.fetch_balance())

# sell one ฿ for market price and receive $ right now
print(exmo.id, exmo.create_market_sell_order('BTC/USD', 1))

# limit buy BTC/EUR, you pay €2500 and receive ฿1  when the order is closed
print(exmo.id, exmo.create_limit_buy_order('BTC/EUR', 1, 2500.00))

# pass/redefine custom exchange-specific order params: type, amount, price, flags, etc...
kraken.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})

# hitbtc_markets is dictionary type
print(hitbtc_markets["ZEC/USDT"])
'''