import numpy as np
from constants import Constants

class TrendPredictor():
    def __init__(self):
        pass

    def predict_sma(self, stock_current_price, sma_report):
        last_sma9 = sma_report[Constants.MOST_RECENT_SMA9]
        last_sma12 = sma_report[Constants.MOST_RECENT_SMA12]
        last_sma21 = sma_report[Constants.MOST_RECENT_SMA21]
        last_sma60 = sma_report[Constants.MOST_RECENT_SMA60]
        last_sma90 = sma_report[Constants.MOST_RECENT_SMA90]
        
        if last_sma9 > last_sma12 > last_sma21 > last_sma60 > last_sma90:
            trend = "strong uptrend"
        elif last_sma9 < last_sma12 < last_sma21 < last_sma60 < last_sma90:
            trend = "strong downtrend"
        else:
            trend = "sideways / consolidation"

        # Detect SMA crossovers (Golden Cross / Death Cross)
        buy_signal = (last_sma9 > last_sma12 and last_sma12 > last_sma21) and (last_sma9 > last_sma60 and last_sma9 > last_sma90)
        sell_signal = (last_sma9 < last_sma12 and last_sma12 < last_sma21) and (last_sma9 < last_sma60 and last_sma9 < last_sma90)

        # Momentum check (distance between short SMAs)
        momentum = abs(last_sma9 - last_sma21)

        # **Incorporating `current_price` for prediction**
        if stock_current_price > last_sma9 and buy_signal:
            prediction = "Bullish - Buy Signal 📈 (Price above SMAs)"
        elif stock_current_price < last_sma9 and sell_signal:
            prediction = "Bearish - Sell Signal 📉 (Price below SMAs)"
        elif stock_current_price > last_sma60 and stock_current_price > last_sma90:
            prediction = "Bullish - Price above long-term SMAs 🚀"
        elif stock_current_price < last_sma60 and stock_current_price < last_sma90:
            prediction = "Bearish - Price below long-term SMAs 🔻"
        elif momentum < np.mean([last_sma12, last_sma21]) * 0.001:  # If SMA differences are minimal
            prediction = "Neutral - No strong movement ⚖️"
        else:
            prediction = f"Market in {trend}, wait for confirmation."

        return prediction

    def predict_ema(self, stock_current_price, ema_report):
        return "EMA - yet to implement"

    def predict_macd(self, stock_current_price, macd_report):
        return "MACD - yet to implement"


if __name__ == "main":    
    print(TrendPredictor().predict_sma())
