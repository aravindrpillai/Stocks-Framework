import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.fast_info["lastPrice"]


ticker_symbol = "AAPL"
price = get_stock_price(ticker_symbol)
print(price)
