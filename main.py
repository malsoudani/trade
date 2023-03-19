import alpaca_backtrader_api as alpaca
import backtrader as bt
from strategies.adjusted_macd import *
from datetime import datetime
from local_settings import alpaca_paper

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

fromdate = datetime(2021, 3, 31)
todate = datetime.now()

tickers = ['SPY']
timeframes = {
    '15MIN': 15,
}

cerebro = bt.Cerebro()

store = alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER,
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
            fromdate=fromdate,
            todate=todate,
            historical=True,
            backfill_start=True,
        )

        cerebro.adddata(d)

# cerebro.addsizer(bt.sizers.SizerFix, stake=1)
cerebro.addstrategy(AdjustedMACD)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.0)
cerebro.run()

print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
# cerebro.plot(style='candlestick', barup='green', bardown='red')