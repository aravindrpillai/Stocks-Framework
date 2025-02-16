class TrendAnalyser():
    def __init__(self, ticker, data, last_price, round_to = 4):
        self.ticker = ticker
        self.data = data
        self.current_price = last_price
        print(self.current_price)
        self.round_to = round_to

    '''
    'Main Function
    '''
    def analyse(self):
        sma9, sma12, sma21, sma60, sma90 = self.__sma__()
        ema9, ema12, ema21, ema60, ema90 = self.__ema__()
        last_macd, last_signal, last_histogram, previous_histograms = self.__macd__()

        result = {
            "sma9": sma9,
            "sma12": sma12,
            "sma21": sma21,
            "sma60": sma60,
            "sma90": sma90,
            "ema9": ema9,
            "ema12": ema12,
            "ema21": ema21,
            "ema60": ema60,
            "ema90": ema90,
            "macd": last_macd,
            "signal": last_signal,
            "histogram": last_histogram,
            "previous_histograms": previous_histograms
        }

        return result

    '''
    ' SMA - Simple Moving Average
    ' The average price over a set period (a Day, Week or Month).
	' This smoothens the price data and identify the overall trend direction.
	' Used to confirm occured trends so far.
    '''
    def __sma__(self):
        self.data["sma9"] = self.data["Close"].rolling(window=9).mean()
        self.data["sma12"] = self.data["Close"].rolling(window=12).mean()
        self.data["sma21"] = self.data["Close"].rolling(window=21).mean()
        self.data["sma60"] = self.data["Close"].rolling(window=60).mean()
        self.data["sma90"] = self.data["Close"].rolling(window=90).mean()
        last_sma9 = round(float(self.data["sma9"].iloc[-1]), self.round_to)
        last_sma12 = round(float(self.data["sma12"].iloc[-1]), self.round_to)
        last_sma21 = round(float(self.data["sma21"].iloc[-1]), self.round_to)
        last_sma60 = round(float(self.data["sma21"].iloc[-1]), self.round_to)
        last_sma90 = round(float(self.data["sma21"].iloc[-1]), self.round_to)
        return last_sma9, last_sma12, last_sma21, last_sma60, last_sma90


    '''
    ' EMA - Exponential Moving Averages 
    '   09-day EMA (shorter) → Reacts quicker to price changes. (intraday)
    '   12-day EMA (shorter) → Reacts faster to price changes.  (swing)
    '   26-day EMA (longer)  → Reacts slower to price changes   (longterm)
    '''
    def __ema__(self):
        self.data["ema9"] = self.data["Close"].ewm(span=9, adjust=False).mean()
        self.data["ema12"] = self.data["Close"].ewm(span=12, adjust=False).mean()
        self.data["ema21"] = self.data["Close"].ewm(span=21, adjust=False).mean()
        self.data["ema60"] = self.data["Close"].ewm(span=60, adjust=False).mean()
        self.data["ema90"] = self.data["Close"].ewm(span=90, adjust=False).mean()
        last_ema9 = round(float(self.data["ema9"].iloc[-1]), self.round_to)
        last_ema12 = round(float(self.data["ema12"].iloc[-1]), self.round_to)
        last_ema21 = round(float(self.data["ema21"].iloc[-1]), self.round_to)
        last_ema60 = round(float(self.data["ema60"].iloc[-1]), self.round_to)
        last_ema90 = round(float(self.data["ema90"].iloc[-1]), self.round_to)
        return last_ema9, last_ema12, last_ema21, last_ema60, last_ema90


        
    '''
    ' Moving Average Convergence Divergence (MACD)
    ' Used as a trend-following momentum indicator that helps identify buy and sell signals. 
    ' It measures the relationship between two moving averages of a stock’s price.
    ' 
    ' MACD consists of three components:
    '     1. MACD Line (Fast-moving average)
    '         MACD = EMA12 - EMA26
    '     
    '     2. Signal Line (Slower-moving average)
    '         SignalLine = 9 Day EMA of the MACD Line
    '         This helps to smoothen out the fluctuations on the MACD Line
    '     
    '     3. MACD Histogram
    '         Histogram = MCAD - SignalLine 
    '          * Histogram > 0 → Bullish momentum (Buy signal)
    '          * Histogram < 0 → Bearish momentum (Sell signal)
    ' 
    ' MACD Line crosses above Signal Line	📈 Buy Signal	       Trend is turning bullish
    ' MACD Line crosses below Signal Line	📉 Sell Signal	       Trend is turning bearish
    ' MACD Line is above zero	            🔼 Bullish Market	   Momentum is strong upwards
    ' MACD Line is below zero	            🔽 Bearish Market	   Momentum is weak/downtrend
    ' MACD Histogram expands	            🚀 Strong Trend	       Momentum is increasing
    ' MACD Histogram contracts	            ⚠️ Weakening Trend	   Momentum is slowing down
    '''
    def __macd__(self):
        macd_line = self.data["Close"].ewm(span=12, adjust=False).mean() - self.data["Close"].ewm(span=26, adjust=False).mean()
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram_line = macd_line - signal_line
        last_histogram_line = round(histogram_line.iloc[-1], self.round_to)

        last_macd = round(float(macd_line.iloc[-1]), self.round_to)
        last_signal = round(float(signal_line.iloc[-1]), self.round_to)
        last_histogram_line = round(float(histogram_line.iloc[-1]), self.round_to)
        previous_histograms = [round(float(val), self.round_to) for val in histogram_line.iloc[-6:].tolist()]
        
        return last_macd, last_signal, last_histogram_line, previous_histograms



'''
' Use below for TESTING
'''
if __name__ == "__main__":
    import yfinance as yf   
    ticker = "RELIANCE.NS"
    period = "60d"
    interval = "5d"
    stock = yf.Ticker(ticker)
    last_price = stock.fast_info["lastPrice"]
    data = stock.history(period=period, interval=interval)
    trend = TrendAnalyser(ticker, data, last_price, 4)
    print(trend.analyse())