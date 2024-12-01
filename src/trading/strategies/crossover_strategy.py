from enum import Enum
import numpy as np
from trading.indicators.base_indicator import BaseIndicator
from trading.strategies.base_strategy import BaseStrategy


class CrossoverStrategy(BaseStrategy):
    def __init__(self, data, short_period, long_period):
        super().__init__(data)
        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(
        self, indicator: BaseIndicator, mode: Enum, column_indicator: str = "Close"
    ):
        """
        Generate signals based on Indicator crossover.
        """
        indicator_instance = indicator(self.data[column_indicator])
        self.data["short_period"] = indicator_instance.calculate(
            self.short_period, mode=mode
        )
        self.data["long_period"] = indicator_instance.calculate(
            self.long_period, mode=mode
        )

        self.data["signal"] = 0
        self.data["signal"][self.short_period :] = np.where(
            self.data["short_period"][self.short_period :]
            > self.data["long_period"][self.short_period :],
            1,
            0,
        )
        self.data["positions"] = self.data["signal"].diff()
        return self.data
