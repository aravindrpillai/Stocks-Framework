import yfinance as yf
from trend_analyser import TrendAnalyser

ticker = "RELIANCE.NS"
period = "1d"
interval = "5m"

stock = yf.Ticker(ticker)
data = stock.history(period=period, interval=interval)

trend = TrendAnalyser(ticker, data).analyse()
print(trend)