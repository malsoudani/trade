import backtrader as bt
import datetime

class AdjustedMACD(bt.Strategy):
    def __init__(self):
        self.order = None
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.AdaptiveMovingAverage)
        self.macd = bt.indicators.MACD(self.datas[0])
        # self.macd = bt.indicators.MACD(self.datas[0], period_me1=24, period_me2=52, period_signal=18)
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.TripleExponentialMovingAverage)
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.DoubleExponentialMovingAverage)
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.MovingAverageSimple)
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.WeightedMovingAverage)
        # self.macd = bt.indicators.MACD(self.datas[0], movav=bt.indicators.SmoothedMovingAverage)

        self.macdcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        # self.rsi = bt.indicators.RSI_EMA(self.datas[0], upperband=80, lowerband=20, period=28)
        self.ema200 = bt.indicators.ExponentialMovingAverage(self.datas[0], period=200)
        self.order = None
        self.dataclose = self.datas[0].close

    def next(self):

        if not self.datas[0].datetime.time(0).second == 0:
            return

        # if not self.time_in_range(datetime.time(14, 30, 0), datetime.time(20, 50, 0), self.datas[-1].datetime.time(0)):
        #     self.close()
        #     return


        # if self.macdcross[-1]:
        #     if self.macdcross[-1] > 0: # buy signal
        #         if self.dataclose[-1] > self.ema200[-1]:
        #             if self.position != 0:
        #                 self.close()
        #             self.order = self.buy()
        #         elif self.dataclose[-1] < self.ema200[-1]:
        #             self.close()
        #     elif self.macdcross[-1] < 0: # sell signal
        #         if self.dataclose[-1] > self.ema200[-1]:
        #             self.close()
        #         elif self.dataclose[-1] < self.ema200[-1]:
        #             if self.position != 0:
        #                 self.close()
        #             self.order = self.sell()
        print(f'{self.data.datetime.date(0)} {self.datas[0].datetime.time(0)} {self.dataclose[0]}');
        # print(f'{self.dataclose[0]}');
        print(f'last MACD cross {self.macdcross[-1]}');
        if self.macdcross[-1]:
            if self.macdcross[-1] > 0: # buy signal
                    print(f'buying at {self.dataclose[0]}');
                    self.close()
                    self.order = self.buy()
            elif self.macdcross[-1] < 0: # sell signal
                    print(f'selling at {self.dataclose[0]}');
                    self.close()
                    self.order = self.sell()

    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end    