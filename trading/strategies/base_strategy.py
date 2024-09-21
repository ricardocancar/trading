from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    def __init__(self, data):
        """
        Base class for all trading strategies.

        :param data: pandas DataFrame containing price data.
        """
        self.data = data.copy()
    
    @abstractmethod
    def generate_signals(self):
        """
        Abstract method to generate trading signals.
        """
        pass
