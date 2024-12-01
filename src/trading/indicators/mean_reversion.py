import pandas as pd

from trading.indicators.base_indicator import BaseIndicator


class MeanReversion(BaseIndicator):
    def __init__(self, data, period=20, num_std_dev=2):
        """
        Inicializa el indicador de Bollinger Bands.

        :param period: Número de periodos para la media móvil.
        :param num_std_dev: Número de desviaciones estándar para las bandas superior e inferior.
        """
        super().__init__(data)
        self.period = period
        self.num_std_dev = num_std_dev

    def calculate(self):
        """
        Calcula las bandas de Bollinger para una serie de precios.

        :param self.data: Serie de precios (pandas Series o lista).
        :return: DataFrame con las columnas ['Middle Band', 'Upper Band', 'Lower Band']
        """

        middle_band = self.data.rolling(window=self.period).mean()
        rolling_std = self.data.rolling(window=self.period).std()

        upper_band = middle_band + (rolling_std * self.num_std_dev)
        lower_band = middle_band - (rolling_std * self.num_std_dev)

        return pd.DataFrame(
            {
                "Middle Band": middle_band,
                "Upper Band": upper_band,
                "Lower Band": lower_band,
            }
        )
