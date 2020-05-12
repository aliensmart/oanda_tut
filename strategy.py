import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
import pandas as pd
import os
import numpy
import talib as ta

token = os.environ.get("OANDA_DEMO_API")
client = oandapyV20.API(access_token=token,environment="practice")

def data(instrument):
        """
            Takes an instrument and return the Open High Low Close of the instrument
        """
        params = {"count": 800,"granularity": "M15"} #granularity can be in seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
        candles = instruments.InstrumentsCandles(instrument=instrument,params=params)
        client.request(candles)
        ohlc_dict = candles.response["candles"]
        ohlc = pd.DataFrame(ohlc_dict)
        ohlc_df = ohlc.mid.dropna().apply(pd.Series)
        ohlc_df["volume"] = ohlc["volume"]
        ohlc_df.index = ohlc["time"]
        ohlc_df = ohlc_df.apply(pd.to_numeric)
        return ohlc_df
data = data("EUR_USD")
data.columns = ["open","high","low","close","volume"]
macd, macdsignal, macdhist = ta.MACD(data["close"], fastperiod=12, slowperiod=26, signalperiod=9)

print(macdhist)