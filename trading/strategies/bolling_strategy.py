from pandas import DataFrame
import numpy as np
from trading.indicators.base_indicator import BaseIndicator
from trading.strategies.base_strategy import BaseStrategy


class BollingStrategy(BaseStrategy):
    def __init__(self, data, short_period, long_period):
        super().__init__(data)
        self.short_period = short_period
        self.long_period = long_period
    
    def generate_signals(self, Indicator:BaseIndicator, column_indicator:str='Close') -> DataFrame:
        """
        Determines if there is a potential reversal signal based on Bollinger Bands.

        - **Buy Signal:** Generated if the price falls below the lower band, indicating a possible bounce.
        - **Sell Signal:** Generated if the price rises above the upper band, indicating a potential reversal.

        :param self.data: Price series (pandas Series or list).
        """
        indicator = Indicator(self.data[column_indicator])
        
        bollinger_df = indicator.calculate()
        signals = []

        condiciones = [
            self.data[column_indicator] < bollinger_df['Lower Band'],
            self.data[column_indicator] > bollinger_df['Upper Band']
        ]

        # Definir los valores correspondientes para cada condición
        valores = [1, -1]

        # Aplicar las condiciones y asignar 0 por defecto
        self.data['signal'] = np.select(condiciones, valores, default=0)
        self.data['positions'] = self.data['signal'].diff()
        return self.data
