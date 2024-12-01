from enum import Enum
from trading.indicators.base_indicator import BaseIndicator
import pandas as pd

class MOMENTUM_INDICATORS(Enum):
    RSI = 'rsi'
    STOCH = 'stoch'

class MomentumIndicators(BaseIndicator):
    def __init__(self, data):
        super().__init__(data)
    
    def rsi(self, period:int=14) -> pd.Series:
        """
        Calculate the Relative Strength Index (RSI).
        """
        delta = self.data.diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
        
    def calculate(self, period:int, mode:Enum) -> pd.Series:
        if mode == MOMENTUM_INDICATORS.RSI:
            return self.rsi(period=period)
        else:
            raise ValueError(f"Invalid mode: {mode}")