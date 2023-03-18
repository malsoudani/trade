import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime, timedelta, date
from strategies.adjusted_macd import *
from local_settings import alpaca_paper

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True


cerebro = bt.Cerebro()
cerebro.addstrategy(AdjustedMACD)

store = alpaca_backtrader_api.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER,
    usePolygon=True
)

if not ALPACA_PAPER:
  broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
  cerebro.setbroker(broker)

DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
data0 = DataFactory(
  dataname='SPY', 
  compression=1,
  fromdate=date.today() - timedelta(days=3), 
  timeframe=bt.TimeFrame.Minutes
)
cerebro.adddata(data0)
cerebro.addsizer(bt.sizers.SizerFix, stake=1)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()