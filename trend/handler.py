from trend.analyser import TrendAnalyser
from trend.predictor import TrendPredictor
from constants import Constants

class TrendHandler():
    def __init__(self, ticker, data, current_price):
        self.ticker = ticker
        self.data = data
        self.current_price = current_price
        ta = TrendAnalyser(ticker, data, current_price, 4)
        self.analysed_report = ta.analyse()
        self.prediction_analyser = TrendPredictor()
        
    def do(self):
        sma_prediction = self.prediction_analyser.predict_sma(self.current_price, self.analysed_report[Constants.MOST_RECENT_SMA])
        self.analysed_report[Constants.MOST_RECENT_SMA][Constants.PREDICTION] = sma_prediction
        
        ema_prediction = self.prediction_analyser.predict_ema(self.current_price, self.analysed_report[Constants.MOST_RECENT_EMA])
        self.analysed_report[Constants.MOST_RECENT_EMA][Constants.PREDICTION] = ema_prediction
        
        macd_prediction = self.prediction_analyser.predict_macd(self.current_price, self.analysed_report[Constants.MOST_RECENT_MACD])
        self.analysed_report[Constants.MOST_RECENT_MACD][Constants.PREDICTION] = macd_prediction
        
        return self.analysed_report
