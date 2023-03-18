import alpaca_backtrader_api as alpaca
import backtrader as bt
from strategies.adjusted_macd import *
import pytz
from datetime import datetime, timedelta
from local_settings import alpaca_paper

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

fromdate = datetime(2020, 12, 31)
todate = datetime.now()

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

for ticker in tickers:
    for timeframe, mins in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {mins} minutes.')

        d = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Minutes,
            compression=mins,
            fromdate=fromdate - timedelta(minutes=200 * 9 * mins),
            todate=todate,
            historical=True,
            backfill_start=True,
        )

        cerebro.adddata(d)

cerebro.addsizer(bt.sizers.SizerFix, stake=1)
cerebro.addstrategy(AdjustedMACD)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.0)
cerebro.run()

print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')