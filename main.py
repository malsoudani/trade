import alpaca_backtrader_api as alpaca
import backtrader as bt
from strategies.adjusted_macd import *
import pytz
from datetime import datetime, timedelta
from local_settings import alpaca_paper
import pandas as pd

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

fromdate = datetime(2020, 12, 28)
todate = datetime(2020, 12, 29)

startdate = fromdate
enddate = todate
delta = timedelta(days=1)

tickers = ['SPY']
timeframes = {
    '5MIN': 5,
}

cerebro = bt.Cerebro()

store = alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER,
    usePolygon=True
)

if not ALPACA_PAPER:
    print(f"LIVE TRADING")
    broker = store.getbroker()
    cerebro.setbroker(broker)

DataFactory = store.getdata

df = pd.DataFrame

movavdict = {
    'simple': {'movav': bt.indicators.MovingAverageSimple},
    'exponential': {'movav': bt.indicators.ExponentialMovingAverage},
    'triple_expo': {'movav': bt.indicators.TripleExponentialMovingAverage},
    'double_expo': {'movav': bt.indicators.DoubleExponentialMovingAverage},
    'wilder': {'period_me1': 24, 'period_me2': 52, 'period_signal': 18},
    'smooth': {'movav': bt.indicators.SmoothedMovingAverage},
    'weighted': {'movav': bt.indicators.WeightedMovingAverage},
    'adaptive': {'movav': bt.indicators.AdaptiveMovingAverage},
}

profit_table = []
counter = 0

while startdate <= enddate:
    movavrow = dict(date=startdate)
    for movavname, movavargs in movavdict.items():
        for ticker in tickers:
            for timeframe, mins in timeframes.items():
                print(f'Adding ticker {ticker} using {timeframe} timeframe at {mins} minutes.')

                d = DataFactory(
                    dataname=ticker,
                    timeframe=bt.TimeFrame.Minutes,
                    compression=mins,
                    fromdate=startdate - timedelta(minutes=200 * 8 * mins),
                    todate=startdate + delta ,
                    historical=True,
                    backfill_start=True,
                )

                cerebro.adddata(d)

        cerebro.addsizer(bt.sizers.SizerFix, stake=1)
        cerebro.addstrategy(AdjustedMACD,macdargs=movavargs)
        cerebro.broker.setcash(0.001)
        cerebro.broker.setcommission(commission=0.0)
        cerebro.run(tradehistory=True)
        movavrow[movavname] = cerebro.broker.getvalue()

    profit_table.append(movavrow)
    startdate += delta

df = pd.DataFrame(profit_table)
df.to_csv('./research_results.csv', index=False)
# print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
# cerebro.plot(style='candlestick', barup='green', bardown='red')