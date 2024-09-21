from enum import Enum
import numpy as np
from trading.indicators.base_indicator import BaseIndicator
from trading.strategies.base_strategy import BaseStrategy


class CrossoverStrategy(BaseStrategy):
    def __init__(self, data, short_period, long_period):
        super().__init__(data)
        self.short_period = short_period
        self.long_period = long_period
    
    def generate_signals(self, Indicator:BaseIndicator, mode:Enum):
        """
        Generate signals based on Indicator crossover.
        """
        indicator = Indicator(self.data['Close'])
        self.data['short_period'] = indicator.calculate(self.short_period, mode=mode)
        self.data['long_period'] = indicator.calculate(self.long_period, mode=mode)
        
        self.data['signal'] = 0
        self.data['signal'][self.short_period:] = \
            np.where(
                self.data['short_period'][self.short_period:] > self.data['long_period'][self.short_period:], 
                1, 0)
        self.data['positions'] = self.data['signal'].diff()
        return self.data

