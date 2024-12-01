import pandas as pd


class BaseIndicator:
    def __init__(self, data):
        """
        Base class for all indicators.

        :param data: pandas Series or DataFrame containing price data.
        """
        if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
            self.data = data.copy()
        else:
            self.data = pd.Series(data)
