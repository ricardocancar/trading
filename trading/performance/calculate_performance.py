import numpy as np
from pandas import DataFrame
from trading.performance.base_performance import BasePerformance


class Performance(BasePerformance):
    def __init__(self, data: DataFrame, risk_free_rate: float = 0.0) -> None:
        super().__init__(data)

    def calculate_returns(self):
        self.data['returns'] = self.data['Close'].pct_change()
        self.data['strategy_returns'] = self.data['returns'] * self.data['signal'].shift(1)
        return self.data

    def calculate_risk(self):
        return (self.data[['returns', 'strategy_returns']].apply(np.exp) - 1).std() * 252 ** 0.5

    def calculate_drawdown(self) -> DataFrame:
        self.data['cumret'] = self.data['strategy_returns'].cumsum().apply(np.exp)
        self.data['cummax'] = self.data['cumret'].cummax()
        self.data['drawdown'] = self.data['cummax'] - self.data['cumret']
        return self.data

    def calculate_performance(self):
        self.calculate_returns()
        self.calculate_drawdown()
        return self.data
