import time, base64, hmac, hashlib, requests, json

'''
Ticker

pair: Requested pair symbol
pairNormalized: Requested pair symbol with "_" in between.
timestamp: Current Unix time in milliseconds
last: Last price
high: Highest trade price in last 24 hours
low: Lowest trade price in last 24 hours
bid: Highest current bid
ask: Lowest current ask
open: Price of the opening trade in last 24 hours
volume: Total volume in last 24 hours
average: Average Price in last 24 hours
daily: Price change in last 24 hours
dailyPercent: Price change percent in last 24 hours
denominatorSymbol: Denominator currency symbol of the pair
numeratorSymbol: Numerator currency symbol of the pair
'''
base = "https://api.btcturk.com"
method = "/api/v2/ticker?pairSymbol=BTC_TRY"
uri = base+method

result = requests.get(url=uri)
result = result.json()
print(json.dumps(result, indent=2))