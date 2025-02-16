import yfinance as yf
from trend.handler import TrendHandler
import json

ticker = "RELIANCE.NS"
period = "1d"
interval = "5m"

stock = yf.Ticker(ticker)
data = stock.history(period=period, interval=interval)
current_price = stock.fast_info["lastPrice"]

trend_report = TrendHandler(ticker, data, current_price).do()
print(json.dumps(trend_report))