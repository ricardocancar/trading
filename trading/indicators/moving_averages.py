import numpy as np
import pandas as pd
from trading.indicators.base_indicator import BaseIndicator
from enum import Enum


class MOVING_AVERAGES(Enum):
    SMA = 'sma'
    EMA = 'ema'
    WMA = 'wma'
    HMA = 'hma'

class MovingAverages(BaseIndicator):
    def __init__(self, data):
        super().__init__(data)
    
    def sma(self, period:int) -> pd.Series:
        """
        Calculate the Simple Moving Average (SMA).
        """
        return self.data.rolling(window=period).mean()
    
    def ema(self, period:int, adjust:float=False) -> pd.Series:
        """
        Calculate the Exponential Moving Average (EMA).
        """
        return self.data.ewm(span=period, adjust=adjust).mean()

    def wma(self, period:int) -> pd.Series:
        """
        Calculate the Weighted Moving Average (WMA).
        """
        weights = np.arange(1, period + 1)
        return self.data.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

    def hma(self, period:int) -> pd.Series:
        """
        Calculate the Hull Moving Average (HMA).
        """
        return self.data.rolling(window=period).apply(lambda x: np.sqrt(np.dot(x, x) / period), raw=True)
    
    def calculate(self, period:int, mode:Enum) -> pd.Series:
        """
        Calculate all moving averages.
        """
        if mode == MOVING_AVERAGES.SMA.value:
            return self.sma(period=period)
        elif mode == MOVING_AVERAGES.EMA.value:
            return self.ema(period=period)
        elif mode == MOVING_AVERAGES.WMA.value:
            return self.wma(period=period)
        elif mode == MOVING_AVERAGES.HMA.value:
            return self.hma(period=period)
        else:
            raise ValueError(f"Invalid mode: {mode}")


        
